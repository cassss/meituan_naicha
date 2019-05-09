# -*- coding: utf-8 -*-
import scrapy,random,time,json,pymongo,math,re
from scrapy import Request
from meituan.items import ShopInfoItem
from scrapy.conf import settings

class ShopPhoneSpider(scrapy.Spider):
    name = 'shop_phone'
    
    serach_url = "https://www.meituan.com/meishi/%d/"

    def start_requests(self):
        client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        db = client[settings['MONGO_DB']]  # 获得数据库的句柄
        shop = db["new_naicha"]
        for shop_info in shop.find({"phone":None},{ "shop_id": 1}):
            shop_id = shop_info["shop_id"]
            yield Request(self.serach_url%(shop_id), callback=self.parse)
            break

    def parse(self, response):
        shop_item = ShopInfoItem()
        res = response.body.decode()
        print(res)
        # js = json.loads(res)
        # searchResult = js["data"]["searchResult"]
        # count = int(js["data"]["totalCount"])
        
        # for shop in searchResult:
        #     if shop["id"] not in self.has_shop:
                
        #         self.rds.lpush("shop_ids", shop["id"])
        #         yield shop_item