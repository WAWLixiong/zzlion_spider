from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

import re
from urllib.parse import urlencode,unquote
import requests
import os
from queue import Queue

class Mumu():

    def __init__(self):
        self.headers={
    'Referer': 'http://mm.tumeitu.net/ti/i.y?site=000000',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
        self.base_url='http://api.mm.tumeitu.net/meitu-back/search.type?pno={pno}&psize=10&'#&varName=idx_{time}
        self.queue=Queue()
        self.pool = Pool()

        meinv_list=['气质','古典','清纯','性感','美腿','制服','嫩模','丝袜']
        nvshen_list=['女神']
        nanshen_list=['潮人','校草','男明星','男模特']
        mengchong_list=['其他宠物','兔子','汪星人','喵星人','宠物鼠']
        sheying_list=['唯美','人文','家装','loml','风景','时尚']
        dongman_list=['cg插画','古风','cosplay','二次元','日本cg']
        bizhi_list=['花卉植物','文字控','风光','炫图','明星','小清新','萌物']

        self.query_dict={'美女':meinv_list,'女神':nvshen_list,'男神':nanshen_list,
                    '萌宠':mengchong_list,'摄影':sheying_list,'动漫':dongman_list,
                         '壁纸':bizhi_list}

    def gen_url(self):
        for keys, values in self.query_dict.items():
            for subName in values:
                params = {
                    'name': keys,
                    'subName': subName
                }
                self.queue.put(self.base_url.format(pno=0)+urlencode(params))

    def get_page_count(self):
        url=self.queue.get()
        # print(url)
        cate=re.findall('name=(.*?)&subName=(.*)',url)[0]
        b_cate=unquote(cate[0])
        s_cate=unquote(cate[1])
        response = requests.get(url)
        if response.status_code in [200,]:
            count = response.json().get('count')
            if count:
                page = count // 10
                for i in range(1, page + 1):
                    per_url = url.replace('pno=0','pno={}'.format(i))
                    response = requests.get(per_url, headers=self.headers)
                    if response.status_code in [200,]:
                        self.parse_list(response.json(),b_cate,s_cate)
            self.parse_list(response.json(),b_cate,s_cate)

    def parse_list(self,resp,b_cate,s_cate):
        datas_list=resp.get('datas')
        if len(datas_list):
            for data in datas_list:
                title= data.get('title')
                down_urls = data.get('downImageUrls')
                for url in down_urls:
                    self.save_image(url, title, down_urls.index(url),b_cate,s_cate)

    def save_image(self,url,title,index,b_cate,s_cate):
        # print(url)
        response=requests.get(url,headers=self.headers)
        if response.status_code in [200,]:
            resp=response.content
            if not os.path.exists(r'images/{}/{}'.format(b_cate,s_cate)):
                os.mkdir(r'images/{}/{}'.format(b_cate, s_cate))
            try:
                with open(r'images/{}/{}/{}_{}.jpg'.format(b_cate,s_cate,title,index),'wb') as f:
                    f.write(resp)
            except Exception as e:
                print(e)

    def _call(self,temp):
        if not self.queue.empty():
            self.pool.apply_async(self.get_page_count,callback=self._call)
    def start(self):

        self.gen_url()
        for i in range(4):
            self.pool.apply_async(self.get_page_count,callback=self._call)
        self.pool.join()

if __name__ == '__main__':
    mumu=Mumu()
    mumu.start()
