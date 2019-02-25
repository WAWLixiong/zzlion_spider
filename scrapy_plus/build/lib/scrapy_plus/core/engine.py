#引擎
from scrapy_plus.core.scheduler import Scheduler
from scrapy_plus.core.downloader import Downloader
from scrapy_plus.core.pipeline import Pipeline
from scrapy_plus.core.spider import Spider
from..middleware.downloader_middleware import DownloaderMiddleware
from ..middleware.spider_middleware import SpiderMiddleware
from..utils.log import logger
from datetime import datetime

from scrapy_plus.http.response import Response
from scrapy_plus.http.request import Request

class Engine(object):
    """提供整个程序运行的入口
        调用每个模块的接口，实现对象传递
    """

    def __init__(self,spider):
        '''
        初始化爬虫以及各种core模块
        :param spider:将要启动的spider
        '''
        self.spider=spider
        self.scheduler=Scheduler()
        self.downloader=Downloader()
        self.pipeline=Pipeline()
        self.spidermiddleware=SpiderMiddleware()
        self.downloadermiddleware=DownloaderMiddleware()
        self.total_requeset_nums=0 #总的请求数
        self.total_response_nums=0 #总的响应数

    def __start_request(self):
        '''
        调用爬虫的start_urls地址，获取所有返回值，加入scheduler队列
        :return:None
        '''
        # 1.调用爬虫的start_request方法，得到初始的请求
        for start_request in self.spider.start_request(): #start_request是一个生成器
            start_request = self.spidermiddleware.process_request(start_request)
            # 2.请求交给调度器保存
            self.scheduler.add_request(start_request)
            self.total_requeset_nums+=1

    def __execute_request_response_item(self):
        '''
        实现一次从调度器取请求，到下载，使用spider的parse方法进行处理，同时管道处理item
        :return:
        '''
        # 3.从调度器中取出请求
        request = self.scheduler.get_request()
        if request is None:
            return
        # 4.把请求传递给下载器下载获取响应
        request = self.downloadermiddleware.process_request(request)
        response = self.downloader.get_response(request)
        #把request保存的meta属性传递给response对象
        response.meta=request.meta
        response = self.downloadermiddleware.process_response(response)

        # 5.响应交给爬虫的parse方法，得到结果
        #根据callback的值，动态的获取解析方法
        parse=getattr(self.spider,request.callback)
        response = self.spidermiddleware.process_response(response)
        for result in parse(response): #parse 方法是一个生成器
        # 6.判断结果是请求，继续交给调度器，如果是数据，交给管道处理
            if isinstance(result, Request):
                result = self.spidermiddleware.process_request(result)
                self.scheduler.add_request(result)
                self.total_requeset_nums+=1
            else:
                self.pipeline.process_item(result)
        self.total_response_nums+=1


    def start(self):
        '''
        让程序启动的入口
        :return:
        '''
        start_time=datetime.now()
        logger.info('爬虫开始启动:{}'.format(start_time))  # info中间不能打逗号
        self.__start_engine()
        end_time=datetime.now()
        logger.info('爬虫结束时间:{}'.format(end_time))
        logger.info('一共花了{}秒'.format((end_time-start_time).total_seconds()))

    def __start_engine(self):
        '''实现具体的流程'''
    #     #1.调用爬虫的start_request方法，得到初始的请求
    #     start_request=self.spider.start_request()
    #     start_request=self.spidermiddleware.process_request(start_request)
    #     #2.请求交给调度器保存
    #     self.scheduler.add_request(start_request)
    #     #3.从调度器中取出请求
    #     request=self.scheduler.get_request()
    #     #4.把请求传递给下载器下载获取响应
    #     request=self.downloadermiddleware.process_request(request)
    #     response=self.downloader.get_response(request)
    #     response=self.downloadermiddleware.process_response(response)
    #     #5.响应交给爬虫的parse方法，得到结果
    #     response=self.spidermiddleware.process_response(response)
    #     result=self.spider.parse(response)
    #     #6.判断结果是请求，继续交给调度器，如果是数据，交给管道处理
    #     if isinstance(result,Request):
    #         result=self.spidermiddleware.process_request(result)
    #         self.scheduler.add_request(result)
    #     else:
    #         self.pipeline.process_item(result)
        self.__start_request()
        while True:
            self.__execute_request_response_item()
            if self.total_response_nums>=self.total_requeset_nums:
                break



