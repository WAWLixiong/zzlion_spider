import threading
from queue import Queue
from urllib.parse import urlencode,unquote
import requests
import re
import os

class Mumu(object):

    def __init__(self):

        self.start_queue=Queue()
        self.parse_queue=Queue()
        self.down_queue=Queue()

        self.base_url = 'http://api.mm.tumeitu.net/meitu-back/search.type?pno={pno}&psize=10&'  # &varName=idx_{time}
        self.headers = {
            'Referer': 'http://mm.tumeitu.net/ti/i.y?site=000000',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        meinv_list = ['气质', '古典', '清纯', '性感', '美腿', '制服', '嫩模', '丝袜']
        nvshen_list = ['女神']
        nanshen_list = ['潮人', '校草', '男明星', '男模特']
        mengchong_list = ['其他宠物', '兔子', '汪星人', '喵星人', '宠物鼠']
        sheying_list = ['唯美', '人文', '家装', 'loml', '风景', '时尚']
        dongman_list = ['cg插画', '古风', 'cosplay', '二次元', '日本cg']
        bizhi_list = ['花卉植物', '文字控', '风光', '炫图', '明星', '小清新', '萌物']

        self.query_dict = {'美女': meinv_list, '女神': nvshen_list, '男神': nanshen_list,
                           '萌宠': mengchong_list, '摄影': sheying_list, '动漫': dongman_list,
                           '壁纸': bizhi_list}

    def start(self):
        for keys, values in self.query_dict.items():
            for subName in values:
                params = {
                    'name': keys,
                    'subName': subName
                }
                self.start_queue.put(self.base_url.format(pno=0) + urlencode(params))

    def  parse_count(self):
        while 1:
            url = self.start_queue.get()
            response = requests.get(url)
            if response.status_code in [200, ]:
                count = response.json().get('count')
                if count:
                    page = count // 10
                    for i in range(1, page + 1):
                        per_url = url.replace('pno=0', 'pno={}'.format(i))
                #         response = requests.get(per_url, headers=self.headers)
                #         if response.status_code in [200, ]:
                #             self.parse_index(response.json(), b_cate, s_cate)
                # self.parse_index(response.json(), b_cate, s_cate)
                        self.parse_queue.put(per_url)
            self.start_queue.task_done()

    def parse_index(self,*args):
        while 1:
            url=self.parse_queue.get()
            cate = re.findall('name=(.*?)&subName=(.*)', url)[0]
            b_cate = unquote(cate[0])
            s_cate = unquote(cate[1])
            response=requests.get(url,headers=self.headers)
            if response.status_code in[200,]:
                datas_list = response.json().get('datas')
                if len(datas_list):
                    for data in datas_list:
                        item={}
                        item['title'] = data.get('title')
                        down_urls = data.get('downImageUrls')
                        for url in down_urls:
                            item['url']=url
                            item['b']=b_cate
                            item['s']=s_cate
                            item['index']=down_urls.index(url)
                            self.down_queue.put(item)
                            # self.down(url, title, down_urls.index(url), b_cate, s_cate)
            self.parse_queue.task_done()

    def down(self):
        while 1:
            item=self.down_queue.get()
            title=item['title']
            url=item['url']
            b_cate=item['b']
            s_cate=item['s']
            index=item['index']
            response = requests.get(url, headers=self.headers)
            self.down_queue.task_done()
            if response.status_code in [200, ]:
                resp = response.content
                if not os.path.exists(r'images/{}/{}'.format(b_cate, s_cate)):
                    os.makedirs(r'D:\05_practice_project\木木多线程\images\{}\{}'.format(b_cate, s_cate))
                try:
                    with open(r'images/{}/{}/{}_{}.jpg'.format(b_cate, s_cate, title, index), 'wb') as f:
                        f.write(resp)
                except Exception as e:
                    print(e)


    def run(self):
        th = []
        thread_1=threading.Thread(target=self.start)
        th.append(thread_1)
        thread_2=threading.Thread(target=self.parse_count)
        th.append(thread_2)
        for i in range(2):
            thread_3 = threading.Thread(target=self.parse_index)
            th.append(thread_3)
        for i in range(3):#RuntimeError: cannot set daemon status of active thread
            thread_4 = threading.Thread(target=self.down)
            th.append(thread_4)

        for t in th:
            t.setDaemon(True)
            t.start()

        qu=[self.start_queue,self.parse_queue,self.down_queue]
        for q in qu:
            q.join()



if __name__ == '__main__':
    mumu=Mumu()
    mumu.run()

