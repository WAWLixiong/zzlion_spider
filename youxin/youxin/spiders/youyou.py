# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from copy import deepcopy

class YouyouSpider(Spider):
    name = 'youyou'
    allowed_domains = ['xin.com']
    start_urls = ['https://m.xin.com/location/index/beijing?abversion=59a_60b&optoken=ab_cache_key_f4c2c656f78d8f17f43575f1892ee847']
    base_url='https://www.xin.com/{city}/s/'

    def parse(self, response):
        dt_list=response.xpath('//section[@class="city-list"]/dl[@class="city-column"]/dt[position()>2]')
        for dt in dt_list:
            item={}
            item['category']=dt.xpath('./text()').extract_first()
            a_list=dt.xpath('./following-sibling::dd/a')
            for a in a_list:
                item['city']=a.xpath('./text()').extract_first()
                item['data_city']=a.xpath('./@data-city').extract_first()
                yield Request(url=self.base_url.format(city=item['data_city']),
                              callback=self.parse_list,meta={'item':deepcopy(item)})

    def parse_list(self,response):
        item=response.meta.get('item')
        li_list=response.xpath('//div[@class="_list-con list-con clearfix ab_carlist"]/ul/li')
        if li_list:
            for li in li_list:
                item['title']=li.xpath('.//h2/span/text()').extract_first()
                car_url='https:'+li.xpath('.//h2/span/@href').extract_first()
                yield Request(url=car_url,callback=self.parse_detail,
                              meta={'item':deepcopy(item)})
        next=response.xpath('div[@class="con-page search_page_link"]/a[last()]')
        if next.extract_first()=='下一页':
            next_url=next.xpath('./@href').exract_first()
            yield response.follow(url=next_url,callback=self.parse_list,
                                  meta={'item':deepcopy(item)})

    def parse_detail(self,response):
        item=response.meta.get('item')
        item['price']=response.xpath('//span[@class="cd_m_info_jg"]/b/text()').extract_first()
        item['license_time']=response.xpath('//ul[@class="cd_m_info_desc"]/li[1]/span/text()').extract()
        div=response.xpath('//div[@class="cd_m_i_pz"]')
        if div:
            dl_1=div.xpath('./dl[1]')
            item['emission_standard']=dl_1.xpath('./dd[1]/span[2]/text()').extract_first().strip()
            item['express_mileage']=dl_1.xpath('./dd[2]/span[2]//text()').extract()
            item['nature_of_use']=dl_1.xpath('./dd[3]/span[2]/text()').extract_first().strip()
            item['annual_inspection']=dl_1.xpath('./dd[4]/span[2]/text()').extract_first().strip()
            item['insurance']=dl_1.xpath('./dd[5]/span[2]/text()').extract_first().strip()
            item['maintenance']=dl_1.xpath('./dd[6]/span[2]/text()').extract_first().strip()

            dl_2=div.xpath('./dl[2]')
            item['vehicle_factory']=dl_2.xpath('./dd[1]/span[2]//text()').extract()
            item['vehicle_level']=dl_2.xpath('./dd[2]/span[2]//text()').extract()
            item['vehicle_color']=dl_2.xpath('./dd[3]/span[2]//text()').extract()
            item['vehicle_structure']=dl_2.xpath('./dd[4]/span[2]//text()').extract()
            item['curb_quality']=dl_2.xpath('./dd[5]/span[2]/text()').extract_first().strip()
            item['wheelbase']=dl_2.xpath('./dd[6]/span[2]/text()').extract_first().strip()

            dl_3=div.xpath('./dl[3]')
            item['engine'] = dl_3.xpath('./dd[1]/span[2]/text()').extract_first().strip()
            item['transmission'] = dl_3.xpath('./dd[2]/span[2]//text()').extract()
            item['displacement'] = dl_3.xpath('./dd[3]/span[2]//text()').extract()
            item['fuel_type'] = dl_3.xpath('./dd[4]/span[2]/text()').extract_first().strip()
            item['drive_mode'] = dl_3.xpath('./dd[5]/span[2]/text()').extract_first().strip()
            item['fuel_consumption'] = dl_3.xpath('./dd[6]/span[2]/text()').extract_first().strip()
            yield item