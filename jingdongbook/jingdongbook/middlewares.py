# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import json
import logging
import time


class ProxyDownloaderMiddleware(object):
    # __instance=None

    # def __new__(cls, *args, **kwargs):
    #     if not cls.__instance:
    #         cls.__instance=super().__new__(cls)
    #     return cls.__instance

    def __init__(self):
        self.proxy=None
        self.logger=logging.getLogger(__name__)

    def get_proxy(self):
        url='http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=0fd4e0ddfba24f729775b470199acf23&orderno=YZ20192238979dxZqid&returnType=2&count=1'
        data=json.loads(requests.get(url).content.decode())
        if data.get('ERRORCODE')=='0':
            ip=data.get('RESULT')[0].get('ip')
            port=data.get('RESULT')[0].get('port')
            return str(ip)+':'+str(port)
        return None

    def process_request(self,request,spider):
        # if request.meta.get('retry_time'):
        if self.proxy and request.meta.get('retry_times'):
            self.logger.info('通过请求--使用代理 ' + self.proxy)
            request.meta['proxy']='https://'+self.proxy
        # if request.url.startswith('https://list.jd.com/'):
        #     request.headers['Referer']=request.url


    def process_response(self,request,response,spider):
        body=response.body.decode('gbk','ignore')
        if len(body):
            return response
        else:
            self.proxy =self.get_proxy()
            if self.proxy:
                self.logger.info('通过响应--使用代理 ' + self.proxy)
                request.meta['proxy'] = 'https://' + self.proxy
            return request

