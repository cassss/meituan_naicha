# -*- coding: utf-8 -*-
import scrapy,random,time,json,pymongo,math,re
from scrapy import Request
from meituan.items import ShopCountItem
from scrapy.conf import settings

class ShopInfoSpider(scrapy.Spider):
    name = 'shop_info'
    
    serach_url = "https://apimobile.meituan.com/group/v4/poi/pcsearch/%d?uuid=%s&userid=-1&limit=32&offset=%d&cateId=21329"

    def start_requests(self):
        client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        db = client[settings['MONGO_DB']]  # 获得数据库的句柄
        coll = db["shop_count"]
        has_city = []
        for city in coll.find({},{ "cityId": 1}):
            city_id = city["cityId"]
            has_city.append(city_id)
        coll2 = db["city_info"]
        for city in coll2.find({},{ "cityId": 1}):
            city_id = city["cityId"]
            if city_id not in has_city:
                yield Request(self.serach_url%(city_id, self._getUUId(), 0), callback=self.parse, dont_filter= True)

    def parse(self, response):
        shop_item = ShopCountItem()
        res = response.body.decode()
        js = json.loads(res)
        count = int(js["data"]["totalCount"])
        city_id = re.search(r'/pcsearch/([0-9]+)?', response.url).group(1)
        shop_item["count"] = count
        shop_item["cityId"] = int(city_id)
        yield shop_item
    
    def _getUUId(self):
        return "%s.%d.1.0.0"%(self._ranstr(20), int(time.time()))

    def _ranstr(self, num):
        H = 'abcdefghijklmnopqrstuvwxyz'
        salt = ''
        for i in range(num):
            salt += random.choice(H)

        return salt