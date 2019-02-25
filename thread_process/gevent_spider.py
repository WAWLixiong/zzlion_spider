import gevent.monkey
#打补丁必须放在导入其他模块之前
gevent.monkey.patch_all()

import requests
from lxml import etree
import time
from gevent.pool import Pool
from queue import Queue

class QiuBai():

    def __init__(self):
        self.base_url='https://www.baidu.com/{}'
        self.pool=Pool(5) #一般为核心数量
        self.queue=Queue()
        self.total_request_num=0
        self.total_response_num=0
        self.is_running=True

    def  get_url(self):
        for i in range(5):
            url=self.base_url.format(str(i))
            self.pool.put(url)
            self.total_request_num+=1

    def parse_url(self,url):
        resp=requests.get(url).content.decode()
        if resp.status_code !=200:
            self.queue.put(url)
            self.total_request_num+=1
            return None
        else:
            self.total_response_num+=1
            return resp

    def parse_item(self,resp):
        html=etree.HTML(resp)
        li_list=html.xpath('')
        item={}
        for li in li_list:
            item['name']=li.xpath('')
            item['age']=li.xpath('')
            return item

    def save_item(self,item):
        pass

    def all_course(self):
        url=self.queue.get()
        resp=self.parse_url(url)
        # if  not resp: #这样的话response数量没有加1，导致不会达到平衡
        #     return
        if resp:
            item=self.parse_item(resp)
            self.save_item(item)
        #放在if 外边，不管有没有请求成功都+1
        self.total_response_num+=1


    def __calback(self):
        if self.is_running:
            self.pool.apply_async(self.all_course,callback=self.__calback)

    def run(self):
        self.get_url()
        for i in range(7): #提高并发
            # 通过apply_async能够让函数异步执行，但是只能执行一次，
            # callback是函数执行完成以后的回调函数，指向完成一次之后，再执行一个(请求--保存)循环
            self.pool.apply_async(self.all_course,callback=self.__calback)

        while True:
            time.sleep(0.0001)
            if self.total_response_num >= self.total_request_num:
                self.is_running=False

if __name__ == '__main__':
    qiubai=QiuBai()
    qiubai.run()





