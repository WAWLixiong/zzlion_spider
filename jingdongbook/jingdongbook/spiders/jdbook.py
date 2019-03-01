# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
import json


class JdbookSpider(RedisSpider):
    name = 'jdbook'
    allowed_domains = ['book.jd.com', 'list.jd.com', 'item.jd.com', 'p.3.cn', 'club.jd.com']
    # start_urls = ['https://book.jd.com/booksort.html/']
    price_url = 'https://p.3.cn/prices/mgets?&skuIds=J_{id}'
    comment_url = 'https://club.jd.com/comment/skuProductPageComments.action?score=0&productId={id}&sortType=5&page={page}'
    max_page = 100

    redis_key = 'jdbook'

    def parse(self, response):
        item = {}
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')
        for dt in dt_list:
            item['big_card'] = dt.xpath('./a/text()').extract_first()
            item['big_card_url'] = dt.xpath('./a/@href').extract_first()
            em_list = dt.xpath('./following-sibling::dd/em')
            for em in em_list:
                item['second_card'] = em.xpath('./a/text()').extract_first()
                item['second_card_url'] = 'https:' + em.xpath('./a/@href').extract_first()
                yield Request(url=item['second_card_url'], callback=self.parse_index, meta={'item': deepcopy(item)})

    def parse_index(self, response):
        item = response.meta.get('item')
        li_list = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        for li in li_list:
            item['title'] = li.xpath('.//div[@class="p-name"]/a/em/text()').extract_first().strip()
            item['book_url'] = li.xpath('.//div[@class="p-name"]/a/@href').extract_first()
            yield response.follow(url=item['book_url'], callback=self.parse_detail, meta={'item': deepcopy(item)})
        next = response.xpath('//span[@class="p-num"]/a[@class="pn-next"]/@href').extract_first()
        if next:
            yield response.follow(url=next, callback=self.parse_index,meta={'item': deepcopy(item),
                                                                            'dont_redirect':True,
                                                                            'handle_httpstatus_list':[302]})

    def parse_detail(self, response):
        item = response.meta.get('item')
        li_list = response.xpath('//ul[@id="parameter2"]/li')
        for li in li_list:
            word = li.xpath('.//text()').extract()[0]
            if word.startswith('店铺'):
                item['store'] = li.xpath('./a/text()').extract_first()
                continue
            elif word.startswith('出版社'):
                item['press'] = li.xpath('./a/text()').extract_first()
                continue
            elif word.startswith('ISBN'):
                item['ISBN'] = li.xpath('./@title').extract_first()
                continue
            elif word.startswith('商品编'):
                item['book_id'] = li.xpath('./@title').extract_first()
                continue
            elif word.startswith('丛书名'):
                item['book_name'] = li.xpath('./a/text()').extract_first()
                continue
        try:
            item['book_id']
        except:
            pass
        else:
            yield response.follow(url=self.price_url.format(id=item['book_id']), callback=self.parse_price,
                                  meta={'item': item})

    def parse_price(self, response):
        item = response.meta.get('item')
        data = json.loads(response.body.decode('gbk','ignore'))
        if data[0]:
            item['origin_price'] = data[0].get('op')
            item['sale_price'] = data[0].get('p')
        yield Request(url=self.comment_url.format(id=item['book_id'], page=0), callback=self.parse_maxpage,
                      meta={'item': deepcopy(item)},dont_filter=True)

    def parse_maxpage(self,response):
        item=response.meta.get('item')
        print('_' * 100)
        data=json.loads(response.body.decode('gbk','ignore'))
        print(data)
        print('_' * 100)
        max_page=data.get('maxPage')
        if max_page:
            for i in range(max_page):
                yield Request(url=self.comment_url.format(id=item['book_id'],page=i),
                              callback=self.parse_comment,meta={'item':deepcopy(item)},dont_filter=True)

    def parse_comment(self, response):
        item = response.meta.get('item')
        data = json.loads(response.body.decode('gbk','ignore'))
        comment_list = data.get('comments')
        if len(comment_list):
            for comment in comment_list:
                item['comment_id'] = comment.get('id')
                item['comment'] = comment.get('content')
                item['comment_time'] = comment.get('creationTime')
                yield item

