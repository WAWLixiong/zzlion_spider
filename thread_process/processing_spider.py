import requests
import time
from lxml import etree

#多进程中使用普通队列模块会发生阻塞，对应的需要使用multiprocessing提供的JoinableQueue模块
from multiprocessing import JoinableQueue as Queue
from multiprocessing import Process

class QiuBai():
    def __init__(self):
        self.base_url='https://www.baidu.com/{}'
        self.req_queue=Queue()
        self.res_queue=Queue()
        self.item_queue=Queue()

    def get_url(self):
        for i in range(10):
            self.req_queue.put(self.base_url.format(str(i)))

    def parse_url(self):
        while True:
            url=self.req_queue.get()
            try:
                resp=requests.get(url).content.decode()
            except Exception as e:
                self.req_queue.put(url)
                print(e)
            else:
                if resp.status_code == 200 :
                    self.res_queue.put(url)
                else:
                    self.req_queue.put(url)
            self.req_queue.task_done()

    def parse_item(self):
        while True:
            resp=self.res_queue.get()
            html=etree.HTML(resp)
            li_list=html.xpath('')
            item={}
            for li in li_list:
                item['name']=li.xpath('')
                item['age']=li.xpath('')
                self.item_queue.put(item)
            self.res_queue.task_done()

    def save_item(self):
        while True:
            item=self.item_queue.get()
            self.item_queue.task_done()
            pass

    def run(self):
        threadlist=[]
        t_url=Process(target=self.get_url)

        #遍历发送请求，获取响应
        for i in range(3):
            t_parse=Process(target=self.parse_url)
            threadlist.append(t_parse)

        #提取数据
        for i in range(2):
            t_get_item=Process(target=self.parse_item)
            threadlist.append(t_get_item)

        #保存数据
        t_save=Process(target=self.save_item)
        threadlist.append(t_save)

        for process in threadlist:
            #设置为守护进程
            process.daemon=True
            process.start()

        for q in [self.req_queue,self.res_queue,self.item_queue]:
            q.join() #让主进程阻塞，直到队列任务直接

if __name__ == '__main__':

    qiubai=QiuBai()
    qiubai.run()





