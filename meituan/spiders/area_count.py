# -*- coding: utf-8 -*-
import scrapy,random,time,json,pymongo,math,re
from scrapy import Request
from meituan.items import AreaCountItem
from scrapy.conf import settings

class AreaCountSpider(scrapy.Spider):
    name = 'area_count'
    
    serach_url = "https://apimobile.meituan.com/group/v4/poi/pcsearch/%d?uuid=%s&userid=-1&limit=32&offset=%d&cateId=21329&q=奶茶&areaId=%d"

    def start_requests(self):
        client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        db = client[settings['MONGO_DB']]  # 获得数据库的句柄
        coll = db["area_count"]
        has_area = []
        for area in coll.find({},{ "areaId": 1}):
            areaId = area["areaId"]
            has_area.append(areaId)
        coll2 = db["area_info"]
        for area in coll2.find({},{ "areaId": 1, "cityId": 1}):
            areaId = area["areaId"]
            cityId = area["cityId"]
            if areaId not in has_area:
                yield Request(self.serach_url%(cityId, self._getUUId(), 0, areaId), callback=self.parse, dont_filter= True)

    def parse(self, response):
        shop_item = AreaCountItem()
        res = response.body.decode()
        js = json.loads(res)
        count = int(js["data"]["totalCount"])
        cityId = re.search(r'/pcsearch/([0-9]+)?', response.url).group(1)
        areaId = re.search(r'areaId=([0-9]+)', response.url).group(1)
        shop_item["count"] = count
        shop_item["cityId"] = int(cityId)
        shop_item["areaId"] = int(areaId)
        yield shop_item
    
    def _getUUId(self):
        return "%s.%d.1.0.0"%(self._ranstr(20), int(time.time()))

    def _ranstr(self, num):
        H = 'abcdefghijklmnopqrstuvwxyz'
        salt = ''
        for i in range(num):
            salt += random.choice(H)

        return salt