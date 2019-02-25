#爬虫
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item

class Spider(object):
    """完成基本的爬虫"""
    start_urls=[]

    def start_request(self):
        '''
        发送起始连接，交给引擎
        :return:
        '''
        for url in self.start_urls:
            yield Request(url=url)

    def parse(self,response):
        '''
        处理start_url对应的响应
        :param response:
        :return:
        '''
        yield Item(response.body)