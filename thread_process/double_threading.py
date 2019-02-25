from threading import Thread
import requests
from lxml import  etree
from queue import Queue
import time

class Crawler(object):

    def __init__(self):
        self.base_url='https://www.bai.com/{}'
        self.req_queue=Queue()
        self.res_queue=Queue()
        self.item_queue=Queue()

    def  get_url(self):
        for i in range(10):
            self.req_queue.put(self.base_url.format(str(i)))

    def parse_url(self):
        while True:
            url=self.req_queue.get()
            try:
                resp=requests.get(url).content.decode()
            except Exception as e:
                print(e)
                self.req_queue.put(url)
            else:
                if resp.status_code == 200:
                    self.res_queue.put(resp)
                else:
                    self.req_queue.put(url)
            self.req_queue.task_done()

    def parse_item(self):
        while True:
            resp=self.req_queue.get()
            html=etree.HTML(resp)
            item={}
            li_list=html.xpath('')
            for i in li_list:
                item['name']=i.xpath('')
                item['age']=i.xpath('')
                self.item_queue.put(item)
            self.req_queue.task_done()

    def save_item(self):
        while True:
            item=self.item_queue.get()
            with open('lixiong.txt','w') as f:
                f.write(item)
            self.item_queue.task_done()

    def run(self):
        threa_list=[]
        thread=Thread(target=self.get_url())
        threa_list.append(thread)
        for i in range(3):
            threa_list.append(Thread(target=self.parse_url))

        for i in range(2):
            threa_list.append(Thread(target=self.parse_item))

        save_threa=Thread(target=self.save_item)
        threa_list.append(save_threa)

        for thread in threa_list:
            thread.setDaemon(True)
            thread.start()

        for q in [self.req_queue,self.res_queue,self.item_queue]:
            q.join() #让主进程阻塞，直到队列中的任务执行完毕


if __name__ == '__main__':
    crawler=Crawler()
    crawler.run()


