# -*- coding: utf-8 -*-
from scrapy import Spider,Request
import re
import base64
from fontTools.ttLib import TTFont
from io import BytesIO
from copy import deepcopy


class ZufangSpider(Spider):
    name = 'zufang'
    allowed_domains = ['bj.58.com']
    start_urls = ['https://bj.58.com/chuzu/?utm_source=sem-360-pc&spm=13364719736.3559025503&pagetype=area&PGTID=0d3090a7-0000-1550-44ba-add2c9a3e77d&ClickID=2']


    def parse(self, response):
        res=response.body.decode()
        bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", res)[0]

        room_list=response.xpath('//ul[@class="listUl"]/li')[0:-1]
        for li in room_list:
            if not li.xpath('./@class').extract_first()=='apartments-pkg apartments':
                item={}
                title=li.xpath('./div[@class="des"]/h2/a/text()').extract_first().strip()
                item['title']=self.get_page_show_ret(title,bs64_str)
                price=li.xpath('.//div[@class="money"]/b/text()').extract_first()
                # price_guige=li.xpath('.//div[@class="money"]/b/./text()').extract_first().strip()
                item['price']=self.get_page_show_ret(price,bs64_str)+'元/每月'
                detail_url=li.xpath('./div[@class="des"]/h2/a/@href').extract_first()
                yield response.follow(url=detail_url,callback=self.parse_detail,meta={'item':deepcopy(item)})
        next=response.xpath('//li[@id="bottom_ad_li"]//a[@class="next"]/@href').extract_first()
        if next:
            yield Request(url=next,callback=self.parse)

    def get_page_show_ret(self,str_info,bs64_str):
        font = TTFont(BytesIO(base64.decodebytes(bs64_str.encode())))
        c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
        ret_list = []
        for char in str_info:
            decode_num = ord(char)
            if decode_num in c:
                num = c[decode_num]
                num = int(num[-2:]) - 1
                ret_list.append(num)
            else:
                ret_list.append(char)
        # ret_str_show = ''
        # for num in ret_list:
        #      ret_str_show += str(num)
        ret_list = [str(i) for i in ret_list]
        ret_str_show = ''.join(ret_list)
        return ret_str_show

    def parse_detail(self,response):
        item=response.meta.get('item')
        html=response.body.decode()
        bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", html)[0]
        item['price_info']=response.xpath('//div[@class="house-pay-way f16"]/span[2]/text()').extract_first()
        item['rental_method']=re.findall('租赁方式：</span><span>(.*?)</span>',html)[0]
        room_type=response.xpath('//li/span[text()="房屋类型："]/following-sibling::span/text()').extract_first().replace('&nbsp;','').replace(' ','')
        item['room_type']=self.get_page_show_ret(room_type,bs64_str).replace('\xa0','')
        floor=response.xpath('//li/span[text()="朝向楼层："]/following-sibling::span/text()').extract_first().strip().replace('&nbsp;','')
        item['floor']=self.get_page_show_ret(floor,bs64_str).replace('\xa0','')
        item['community']=response.xpath('//li/span[text()="所在小区："]/following-sibling::span/a/text()').extract_first().strip()
        item['location']=response.xpath('//li/span[text()="所属区域："]/following-sibling::span/a[1]/text()').extract_first().strip()+ ' '+\
                         response.xpath('//li/span[text()="所属区域："]/following-sibling::span/a[2]/text()').extract_first().strip()+ ' '+\
                        response.xpath('//li/span[text()="所属区域："]/following-sibling::em/text()').extract_first().strip()
        item['address']=response.xpath('//li/span[text()="详细地址："]/following-sibling::span/text()').extract_first().strip()
        yield item
