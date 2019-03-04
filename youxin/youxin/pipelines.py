# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from redis import StrictRedis,ConnectionPool
from hashlib import sha1
from scrapy.exceptions import DropItem
from .settings import REDIS_HOST,REDIS_PORT,REDIS_ITEM_KEY
import mmh3


class DealItem(object):

    def process_item(self,item,spider):
        item['express_mileage']=''.join(item['express_mileage']).strip()
        item['vehicle_factory']=''.join(item['vehicle_factory']).strip()
        item['vehicle_level']=''.join(item['vehicle_level']).strip()
        item['vehicle_color']=''.join(item['vehicle_color']).strip()
        item['vehicle_structure']=''.join(item['vehicle_structure']).strip()
        item['transmission']=''.join(item['transmission']).strip()
        item['displacement']=''.join(item['displacement']).strip()
        return item




class YouxinPipeline(object):

    def __init__(self, mongo_host, mongo_port):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.bloomfilter = BloomFilter()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        self.collection = self.client['secondcar']['youxin']

    def process_item(self, item, spider):
        fp = sha1()
        for value in item.values():
            fp.update(str(value).encode())
        fp_value = fp.hexdigest()
        if self.bloomfilter.is_contains(fp_value):
            raise DropItem('item 已经存在')
        else:
            self.bloomfilter.insert(fp_value)
            self.collection.insert_one(dict(item))
            return item

class BloomFilter(object):
    BIT_SIZE = 5000000
    SEEDS = [50, 51, 52, 53, 54, 55, 56]
    key=REDIS_ITEM_KEY

    def __init__(self, ):
        self.db = StrictRedis(host=REDIS_HOST,port=REDIS_PORT)

    def cal_offset(self, content):
        return [mmh3.hash(content, seed) % self.BIT_SIZE for seed in self.SEEDS]

    def is_contains(self, content):
        if not content:
            return False
        locs = self.cal_offset(content)
        return all(True if self.db.getbit(self.key, loc) else False for loc in locs)

    def insert(self, content):
        locs = self.cal_offset(content)
        for loc in locs:
            self.db.setbit(self.key, loc, 1)