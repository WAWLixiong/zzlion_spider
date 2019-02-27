#引擎

from scrapy_plus.conf.settings import ASYNC_TYPE
if ASYNC_TYPE == 'courtine':
    from gevent.pool import Pool as BasePool
    import gevent.monkey
    gevent.monkey.patch_all()

    class Pool(BasePool):
        '''协程池
        使得具有close方法
        使得apply_async方法具有和线程池一样的接口
        '''

        def apply_async(self, func, args=None, kwds=None, callback=None, error_callback=None):
            return super().apply_async(func, args=args, kwds=kwds, callback=callback)

        def close(self):
            '''什么都不需要执行'''
            pass

elif ASYNC_TYPE == 'thread':
    from multiprocessing.dummy import Pool
else:
    raise Exception('不支持的异步方式')

import time

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
from scrapy_plus.conf.settings import SPIDERS,PIPELINES,SPIDER_MIDDLEWARES,DOWN_MIDDLEWARES,CONCURRENT_REQUEST
from scrapy_plus.utils.status_clollector import StatusCollector

import importlib

class Engine(object):
    """提供整个程序运行的入口
        调用每个模块的接口，实现对象传递
    """

    def __init__(self):
        '''
        初始化爬虫以及各种core模块
        :param spider:将要启动的spider
        '''
        self.spiders=self.__auto_import_instance(SPIDERS,is_spider=True)
        self.collector = StatusCollector(list(self.spiders.keys()))

        self.scheduler=Scheduler(self.collector)
        self.downloader=Downloader()
        self.pipelines=self.__auto_import_instance(PIPELINES)#管道引入engine

        self.spidermiddlewares=self.__auto_import_instance(SPIDER_MIDDLEWARES)
        self.downloadermiddlewares=self.__auto_import_instance(DOWN_MIDDLEWARES)

        # self.total_requeset_nums=0 #总的请求数
        # self.total_response_nums=0 #总的响应数

        self.is_running = False
        self.pool=Pool(4)




    def __auto_import_instance(self,path,is_spider=False):
        instance = []
        if is_spider:
            instance={}

        for p in path:
            #模块位置
            module_path=p.rsplit('.',1)[0]
            #类的名字
            cls_name=p.rsplit('.',1)[1]
            #module对象
            ret=importlib.import_module(module_path)
            #类对象
            cls=getattr(ret,cls_name)
            #类同属(name):类实例，构建这样的字典
            if is_spider:
                instance[cls.name]=cls()
            else:
                instance.append(cls())
        print(instance)
        return instance

    def __start_request(self):
        '''
        调用爬虫的start_urls地址，获取所有返回值，加入scheduler队列
        :return:None
        '''
        # 1.调用爬虫的start_request方法，得到初始的请求

        def __fun(spider_name,spider):
            for start_request in spider.start_request(): #start_request是一个生成器
                for spider_middle in self.spidermiddlewares:
                    start_request = spider_middle.process_request(start_request)
                #给开始的请求添加spider_name属性
                start_request.spider_name=spider_name
                # 2.请求交给调度器保存
                self.scheduler.add_request(start_request)
                # self.total_requeset_nums+=1
                #在redis中给请求数量+1
                self.collector.incr(self.collector.request_nums_key)
        for spider_name,spider in self.spiders.items():
            self.pool.apply_async(__fun,args=(spider_name,spider),callback=self.__collect_start_request_nums)

    def __collect_start_request_nums(self,temp):
        '''统计所有爬虫的start_requests的执行数量'''
        #一个爬虫增加一次
        self.collector.incr(self.collector.start_request_nums_key)


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
        for down_middle in self.downloadermiddlewares:
            request = down_middle.process_request(request)
        response = self.downloader.get_response(request)
        #把request保存的meta属性传递给response对象
        response.meta=request.meta
        for down_middle in self.downloadermiddlewares:
            response = down_middle.process_response(response)

        # 5.响应交给爬虫的parse方法，得到结果
        #根据callback的值，动态的获取解析方法
        spider=self.spiders[request.spider_name]

        parse=getattr(spider,request.callback)
        for spider_middle in self.spidermiddlewares:
            response = spider_middle.process_response(response)
        for result in parse(response): #parse 方法是一个生成器
        # 6.判断结果是请求，继续交给调度器，如果是数据，交给管道处理
            if isinstance(result, Request):
                for spider_middle in self.spidermiddlewares:
                    result = spider_middle.process_request(result)
                #对于新产生的request对象，添加spider_name属性
                result.spider_name=request.spider_name
                self.scheduler.add_request(result)
                # self.total_requeset_nums+=1
                self.collector.incr(self.collector.request_nums_key)
            else:
                for pipeline in self.pipelines:
                    #使用result同名变量接收结果，调用下一个管道对result进行处理
                    result=pipeline.process_item(result,spider)
        # self.total_response_nums+=1
        #在redis中给统计响应的数量+1
        self.collector.incr(self.collector.response_nums_key)

    def start(self):
        '''
        让程序启动的入口
        :return:
        '''
        start_time=datetime.now()
        logger.info('爬虫开始启动:{}'.format(start_time))  # info中间不能打逗号
        logger.info('启动的爬虫：\n{}'.format(SPIDERS))
        logger.info('启动的管道：\n{}'.format(PIPELINES))
        logger.info('启动的爬虫中间件：\n{}'.format(SPIDER_MIDDLEWARES))
        logger.info('启动的下载器中间件：\n{}'.format(DOWN_MIDDLEWARES))

        self.__start_engine()

        end_time=datetime.now()
        logger.info('爬虫结束时间:{}'.format(end_time))
        logger.info('一共花了{}秒'.format((end_time-start_time).total_seconds()))
        logger.info('总的请求数量:{}'.format(self.collector.request_nums))
        logger.info('总的响应数量:{}'.format(self.collector.response_nums))
        logger.info('总的重复数量:{}'.format(self.collector.repeat_request_nums))

        #清除redis中保存数量的键清除
        self.collector.clear()

    def __error_callback(self,exception=ValueError):
        try:
            raise ValueError #抛出异常后，才能被日志捕获，并记录到本地
        except Exception as e:
            logger.exception(e)

    def _callback(self,temp):
        if  self.is_running:
            self.pool.apply_async(self.__execute_request_response_item,callback=self._callback)

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

        #控制异步回调的结束
        self.is_running=True

        self.pool.apply_async(self.__start_request,error_callback=self.__error_callback)
        for i in range(CONCURRENT_REQUEST):
            self.pool.apply_async(self.__execute_request_response_item,callback=self._callback)

        # self.__start_request()
        while True:
            time.sleep(0.0001)  # 避免cpu空转，消耗性能
            # self.__execute_request_response_item()

            #主线程执行到这里的时候，总的请求数必须不等于0再推出，方式0+0>=0 推出程序
            # if self.collector.request_nums !=0:

            #通过判断总的start_request的执行完成的数量和爬虫的数量是否相等，能够保证所有的爬虫的start_url地址都被添加到调度器
            if self.collector.start_request_nums == len(self.spiders):
                # print(self.collector.start_request_nums,len(self.spiders))
                if self.collector.response_nums+self.collector.repeat_request_nums>=self.collector.request_nums:
                    self.is_running=False
                    break

        #由于爬虫连接可能与服务器未断开连接，造成程序无法退出，一般不会调用close，join方法
        # self.pool.close()
        # self.pool.join()


