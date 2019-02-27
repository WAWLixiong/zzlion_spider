import time
import pickle

import redis
from six.moves import queue as BaseQueue

from scrapy_plus.conf.settings import REDIS_QUEUE_NAME,REDIS_QUEUE_HOST,REDIS_QUEUE_PORT,REDIS_QUEUE_DB


# 利用redis实现一个Queue，使其接口同python的内置队列接口一致，可以实现无缝转换
class Queue(object):
    """
    A Queue like message built over redis
    """

    Empty = BaseQueue.Empty
    Full = BaseQueue.Full
    max_timeout = 0.3

    def __init__(self, maxsize=0, name=REDIS_QUEUE_NAME, host=REDIS_QUEUE_HOST, port=REDIS_QUEUE_PORT, db=REDIS_QUEUE_DB,
                lazy_limit=True, password=None):
        """
        Constructor for RedisQueue
        maxsize:    an integer that sets the upperbound limit on the number of
                    items that can be placed in the queue.
        lazy_limit: redis queue is shared via instance, a lazy size limit is used
                    for better performance.
        """
        self.name = name
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        self.maxsize = maxsize
        self.lazy_limit = lazy_limit
        self.last_qsize = 0 #列表长度

    def qsize(self):
        '''列表长度'''
        self.last_qsize = self.redis.llen(self.name)
        return self.last_qsize

    def empty(self):
        '''判断列表是否为空，返回bool'''
        if self.qsize() == 0:
            return True
        else:
            return False

    def full(self):
        '''判断列表是否满了，返回bool'''
        if self.maxsize and self.qsize() >= self.maxsize:
            return True
        else:
            return False

    def put_nowait(self, obj):
        '''存入数据库，未满，且lazy会pass；满了会报错；添加成功，返回True'''
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            raise self.Full
        self.last_qsize = self.redis.rpush(self.name, pickle.dumps(obj)) #last_qsize 返回列表长度
        return True

    def put(self, obj, block=True, timeout=None):
        '''未阻塞，就把对象存到redis
            阻塞的话，死循环内尝试将对象存入redis，报满的话，如果设置延时，并且未到延迟时间，休息
            未设置延时，等待全局延迟时间
        '''
        if not block:
            return self.put_nowait(obj)

        start_time = time.time()
        while True:
            try:
                return self.put_nowait(obj)
            except self.Full:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)

    def get_nowait(self):
        '''取出对象，先进先出，返回None，报错，否则取出对象'''
        ret = self.redis.lpop(self.name)
        if ret is None:
            raise self.Empty
        return pickle.loads(ret)

    def get(self, block=True, timeout=None):
        '''未阻塞，调用取出对象方法
            阻塞，死循环下尝试取出对象，捕获空的话，设置了延时，延时，未设置，休息全局延迟时间
        '''
        if not block:
            return self.get_nowait()

        start_time = time.time()
        while True:
            try:
                return self.get_nowait()
            except self.Empty:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)