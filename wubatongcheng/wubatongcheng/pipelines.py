# -*- coding: utf-8 -*-
import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MongoPipeline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url=mongo_url
        self.mongo_db=mongo_db

    #实现从settings模块中提取数据，通过crawler可以拿到全局配置的每个配置信息
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    #在spider开启时被调用
    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_url)
        self.db=self.client[self.mongo_db]

    #复写process_item方法，对item进行处理，实现item插入到mondodb的操作
    def process_item(self,item,spider):
        #item叫什么名字，collection就改成什么名字，比较方便
        # name=item.__class__.__name__
        #self.db['user'].update({'url_token':item['url_token']},{'$set':item},True)，实现去重添加
        self.db['zufang_info'].insert(dict(item))
        #一定要返回item
        return item

    #在spider关闭时被调用
    def close_spider(self,spider):
        #调用mongodb的关闭，释放内存
        return self.client.close()