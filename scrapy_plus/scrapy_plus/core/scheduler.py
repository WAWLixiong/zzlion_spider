#调度器

#利用six模块实现py2和py3的兼容
from six.moves.queue import Queue
from ..utils.log import logger
from scrapy_plus.conf.settings import SCHEDULER_PERSIST
from scrapy_plus.utils.queue import Queue as RedisQueue
from scrapy_plus.utils.set import NoramlFilterContainer,RedisFilterContainer

import six
import w3lib.url
from hashlib import sha1




class Scheduler(object):
    """
    实现调度器的封装
    存储request对象
    对request对象去重
    """
    def __init__(self,collector):

        if SCHEDULER_PERSIST:
            self.queue=RedisQueue()#使用该队列存储request请求
            self.__filter=RedisFilterContainer()
        else:
            self.queue=Queue()
            self.__filter=NoramlFilterContainer()

        # self.repeat_request_nums = 0
        self.collector=collector

    def add_request(self,request):
        '''
        添加request对象到queue队列
        :param request:对象
        :return:
        '''
        #self._filter_request(request)
        if not request.filter :
            #不过滤，直接产生一个指纹属性
            request.fp=self._gen_fp(request)
            self.queue.put(request)
            return
        if self._filter_request(request):
            self.queue.put(request)

    def get_request(self):
        '''
        从queue中取出request对象
        :return:request对象
        '''
        try:
            request=self.queue.get(False) #False 不等待，直接取，没Value会报错
            logger.info(request.url)
        except:
            request= None
        return request


    def _filter_request(self,request):
        '''
        实现对request对象的去重
        :param request:对象
        :return:bool
        '''
        request.fp=self._gen_fp(request)
        if not self.__filter.exists(request.fp):
            #指纹不存在，返回True
            logger.info('发现新的请求：<{} {}>'.format(request.method,request.url))
            self.__filter.add_fp(request.fp)
            return True
        else:#指纹已经存在，返回False
            logger.info('发现重复的请求：<{} {}>'.format(request.method,request.url))
            # self.repeat_request_nums+=1
            self.collector.incr(self.collector.repeat_request_nums_key)
            return False

    def _gen_fp(self,request):
        url=w3lib.url.canonicalize_url(request.url)
        method=request.method.upper()
        data=request.data if request.data is not None else {}
        data=sorted(data.items(),key=lambda x:x[0])

        s1=sha1()
        s1.update(self.__to_bytes(url))
        s1.update(self.__to_bytes(method))
        s1.update(self.__to_bytes(str(data)))

        fp=s1.hexdigest()
        return fp

    @staticmethod
    def __to_bytes(string):
        if six.PY2:
            if isinstance(string,str):
                return string
            else:
                return string.encode('utf-8')
        elif six.PY3:
            if isinstance(string,str):
                return string.encode('utf-8')
            else:
                return string




