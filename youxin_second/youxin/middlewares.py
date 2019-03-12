# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
from youxin.yundama import indetify
import time
import base64
# from urllib

# class YouxinMiddleware(object):
#
#     def __init__(self,service_args=[]):
#         self.browser=webdriver.PhantomJS(service_args=service_args)
#         self.browser.set_window_size(1400,700)
#         self.wait=WebDriverWait(self.browser,15)
#
#     def __del__(self):
#         self.browser.close()
#
#     def process_request(self,request,spider):
#         if request.url=='https://www.xin.com/beijing':
#             self.browser.get(request.url)
#             self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'table')))
#             return HtmlResponse(url=request.url,body=self.browser.page_source,request=request,encoding='utf-8',
#                                 status=200)
#
#     @classmethod
#     def from_crawler(cls,crawler):
#         return cls(
#             service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS')
#         )

class YouxinMiddleware(object):

    def process_request(self,request,spider):
        request.meta['https_proxy']='https://HIXP137QDA58Y7UD:FB3D08F80F2007F1@http-dyn.abuyun.com:9020'

    def process_response(self,request,response,spider):
        if response.status in [302,]:
            url=response.url
            s=requests.session()
            resp=s.get(url).content
            result=indetify(resp)
            data={'t':round(time.time())*1000,
                  'vcode':result}
            s.post(url='https://www.xin.com/checker/validate/',data=data)
            return request
        else:
            return response