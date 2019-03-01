# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import random
import time

class ProxyDownloaderMiddleware(object):

    def __init__(self):
        self.proxy=self.proxy()
        self.logger=logging.getLogger(__name__)

    # def get_proxy(self):
    #     url='http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=0fd4e0ddfba24f729775b470199acf23&orderno=YZ20192238979dxZqid&returnType=2&count=1'
    #     data=json.loads(requests.get(url).content.decode())
    #     if data.get('ERRORCODE')=='0':
    #         ip=data.get('RESULT')[0].get('ip')
    #         port=data.get('RESULT')[0].get('port')
    #         return str(ip)+':'+str(port)
    #     return None

    def proxy(self):
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"
        proxyUser = "HIXP137QDA58Y7UD"
        proxyPass = "FB3D08F80F2007F1"
        proxy = '{}:{}@{}:{}'.format(proxyUser, proxyPass, proxyHost, proxyPort)
        proxies = 'https://' + proxy
        return proxies

    # def process_request(self,request,spider):
    #     self.logger.info('通过请求--使用代理 ')
    #     request.meta['proxy']=self.proxy
        # if request.url.startswith('https://list.jd.com/'):
        #     request.headers['Referer']=request.url

    def get_ua(slef):
        first_num = random.randint(55, 71)
        third_num = random.randint(0, 3200)
        fourth_num = random.randint(0, 140)
        os_type = [
            '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
            '(Macintosh; Intel Mac OS X 10_12_6)'
        ]
        chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

        ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                       '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                      )
        return ua

    def process_request(self,request,spider):
        header={'user-agent':self.get_ua()}
        request.headers['User_Agent']=header
        # request.meta['proxy'] = self.proxy
        # time.sleep(0.2)

    def process_response(self,request,response,spider):
        body=response.text
        if len(body):
            return response
        else:
            self.logger.info('通过响应__使用代理 ')
            request.meta['proxy'] =self.proxy
            return request


