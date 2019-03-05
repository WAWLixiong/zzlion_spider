# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from copy import  deepcopy

class GuaziSpider(Spider):
    name = 'guazi'
    allowed_domains = ['guazi.com']
    start_urls = ['http://www.guazi.com/bj/buy/o1']*4

    def start_requests(self):
        # cookies={'cityDomain': 'anqing', 'antipas': 'Uo1036479363p429S1421nLL0', 'sessionid': '6d4517c5-e610-4381-b625-0846328dc193', 'uuid': 'aca32f86-405e-4131-cc23-5b53d5306510', 'ganji_uuid': '6060192901252269860971', 'clueSourceCode': '%2A%2300', 'cainfo': '%7B%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_a%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22aca32f86-405e-4131-cc23-5b53d5306510%22%7D', 'user_city_id': '127', 'preTime': '%7B%22last%22%3A1551519578%2C%22this%22%3A1551519578%2C%22pre%22%3A1551519578%7D', 'lg': '1'}

        for url in self.start_urls:
            yield Request(url=url,callback=self.parse,)


    def parse(self, response):
        li_list=response.xpath('//div[@class="city-box all-city"]/div/dl[position()>1]')
        for li in li_list:
            item={}
            item['tap']=li.xpath('./dt/text()').extract_first()
            a_list=li.xpath('./dd/a')
            for a in a_list:
                item['location']=a.xpath('./text()').extract_first().strip()
                item['url']='https://www.guazi.com'+a.xpath('./@href').extract_first()+'/o1/'
                print(item)




