import redis
from scrapy_plus.conf import settings
from scrapy_plus.conf.settings import REDIS_SET_HOST,REDIS_SET_PORT,REDIS_SET_DB,REDIS_SET_NAME


class BaseFilterContainer(object):

    def add_fp(self, fp):
        '''往去重容器添加一个指纹'''
        pass

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        pass


class NoramlFilterContainer(BaseFilterContainer):
    '''利用python的集合类型'''

    def __init__(self):
        self._filter_container = set()

    def add_fp(self, fp):
        ''''''
        self._filter_container.add(fp)

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        if fp in self._filter_container:
            return True
        else:
            return False

class RedisFilterContainer(BaseFilterContainer):



    def __init__(self):
        self._redis = redis.StrictRedis(host=REDIS_SET_HOST, port=REDIS_SET_PORT ,db=REDIS_SET_DB)
        self._name = REDIS_SET_NAME

    def add_fp(self, fp):
        '''往去重容器添加一个指纹'''
        self._redis.sadd(self._name, fp)

    def exists(self, fp):
        '''判断指纹是否在去重容器中'''
        return self._redis.sismember(self._name, fp)