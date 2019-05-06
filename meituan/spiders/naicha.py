# -*- coding: utf-8 -*-
import scrapy,random,time,json
from scrapy import Request
from meituan.items import ShopInfoItem

class NaiChaSpider(scrapy.Spider):
    name = 'naicha'
    
    def start_requests(self):
        # city_id = 1
        # start_url = "https://apimobile.meituan.com/group/v4/poi/pcsearch/%d"%(city_id)
        # data = self._getRequestData()
        start_url = "https://apimobile.meituan.com/group/v4/poi/pcsearch/1?uuid=qwertyuioppoiuytrewq.1552977236.1.0.0&userid=-1&limit=32&offset=0&cateId=21329&areaId=13873"
        Request(start_url, callback=self.parse )
        pass

    def parse(self, response):
        print(1)
        # shop_item = ShopInfoItem()
       
        # next_url = response.xpath('//*[@id="deals"]//div[@class="pager"]/a[@gaevent="imt/deal/list/pageNext"]/@href').extract()
        # if next_url:
        #     next_url = ""
        #     yield Request(next_url, callback=self.parse)
        
    # def _getRequestData(self):
    #     return json.dumps({
    #         'uuid':"%s.%d.1.0.0"%(self._ranstr(20),int(time.time())),
    #         'userid':"-1",
    #         'cateid':"21329"
    #     })
    
    # def _ranstr(self, num):
    #     H = 'abcdefghijklmnopqrstuvwxyz'
    #     salt = ''
    #     for i in range(num):
    #         salt += random.choice(H)

    #     return salt