# -*- coding: utf-8 -*-
import pymongo
from redis import StrictRedis,ConnectionPool
from hashlib import sha1
from scrapy.exceptions import DropItem
from .settings import REDIS_URL
import mmh3
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class JingdongbookPipeline(object):
    redis_key = 'jdbook_item_sha1'

    def __init__(self,mongo_host,mongo_port,redis_url):
        self.mongo_host=mongo_host
        self.mongo_port=mongo_port

        # self.redis_url = redis_url
        # self.pool = ConnectionPool.from_url(self.redis_url)
        # self.redis = StrictRedis(connection_pool=self.pool)

        self.bloomfilter=BloomFilter()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            redis_url=crawler.settings.get('REDIS_URL')
        )

    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_host,self.mongo_port)
        self.collection=self.client['jidong']['jdbook']

    # def process_item(self, item, spider):
    #     fp=sha1()
    #     for value in item.values():
    #         fp.update(str(value).encode())
    #     fp_value=fp.hexdigest()
    #     if not self.redis.sismember(self.redis_key,fp_value):
    #         self.redis.sadd(self.redis_key, fp_value)
    #         self.collection.insert_one(dict(item))
    #         return item
    #     else:
    #         raise DropItem('item 已经存在')

    def process_item(self,item,spider):
        fp=sha1()
        for value in item.values():
            fp.update(str(value).encode())
        fp_value=fp.hexdigest()
        if self.bloomfilter.is_contains(fp_value):
            raise DropItem('item 已经存在')
        else:
            self.bloomfilter.insert(fp_value)
            self.collection.insert_one(dict(item))
            return item


    def close_spider(self,spider):
        return self.client.close()

class BloomFilter(object):
    BIT_SIZE = 5000000
    SEEDS = [50, 51, 52, 53, 54, 55, 56]

    def __init__(self,key='bloomfilter'):
        self.redis_url = REDIS_URL
        self.pool = ConnectionPool.from_url(self.redis_url)
        self.db = StrictRedis(connection_pool=self.pool)
        self.key=key

    def cal_offset(self,content):
        return [mmh3.hash(content,seed) % self.BIT_SIZE for seed in self.SEEDS]

    def is_contains(self,content):
        if not content:
            return False
        locs=self.cal_offset(content)
        return all(True if self.db.getbit(self.key,loc) else False for loc in locs)

    def insert(self,content):
        locs=self.cal_offset(content)
        for loc in locs:
            self.db.setbit(self.key,loc,1)
