import requests
from lxml import etree
import re
from multiprocessing import Process,Queue
import time
import random
import json

class Proxies(object):
    """获取HTTPS高匿代理，获取HTTP高匿代理"""

    def __init__(self,page):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }
        self.proxies = []
        self.verify_pro = []
        self.page=page
        # self.get_http_proxies()
        self.get_https_proxies()

    def get_https_proxies(self):
        """获取HTTPS代理"""
        for p in range(1,self.page+1):
            url='https://www.xicidaili.com/wn/%d'% p
            resp=requests.get(url,headers=self.headers).content.decode()
            html=etree.HTML(resp)
            tr_list=html.xpath('//table[@id="ip_list"]/tr')[1:]
            with open('https_proxies.txt','a') as f:
                for tr in tr_list:
                    type=tr.xpath('./td[5]/text()')[0]
                    protocal=tr.xpath('./td[6]/text()')[0]
                    if type == '高匿' and protocal == 'HTTPS':
                        ip=tr.xpath('./td[2]/text()')[0]
                        port=tr.xpath('./td[3]/text()')[0]
                        proxy='https://{ip}:{port}'.format(ip=ip,port=port)
                        f.write(proxy+'\n')

    def get_http_proxies(self):
        """获取HTTP代理"""
        for p in range(1,self.page+1):
            url = 'https://www.xicidaili.com/wt/%d' % p
            resp = requests.get(url, headers=self.headers).content.decode()
            html = etree.HTML(resp)
            tr_list = html.xpath('//table[@id="ip_list"]/tr')[1:]
            with open('http_proxies.txt', 'a') as f:
                for tr in tr_list:
                    type = tr.xpath('./td[5]/text()')[0]
                    protocal = tr.xpath('./td[6]/text()')[0]
                    if type == '高匿' and protocal == 'HTTP':
                        ip = tr.xpath('./td[2]/text()')[0]
                        port = tr.xpath('./td[3]/text()')[0]
                        proxy = 'http://{ip}:{port}'.format(ip=ip, port=port)
                        f.write(proxy + '\n')

    def verify_proxies(self):
        pass

    def verify_one_proxy(self):
        pass

if __name__ == '__main__':
    p=Proxies(4)
