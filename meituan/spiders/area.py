# -*- coding: utf-8 -*-
import scrapy,json,pymongo,re
from scrapy import Request
from meituan.items import AreaItem
from scrapy.conf import settings

class AreaSpider(scrapy.Spider):
    name = 'area'
    
    serach_url = "https://i.meituan.com/%s/all/"

    def start_requests(self):
        client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        db = client[settings['MONGO_DB']]  # 获得数据库的句柄
        coll = db["city_info"]
        for city in coll.find({},{ "pinyin": 1}):
            city_id = city["pinyin"]
            yield Request(self.serach_url%(city_id), callback=self.parse)

    def parse(self, response):
        area_item = AreaItem()
        js = response.xpath('//script[@id="filterData"]/text()').extract()[0]
        cityId = re.search(r"Analytics\('set', 'cityid', ([0-9]+)\);", response.body.decode()).group(1)
        cityId = int(cityId)
        js = json.loads(js)
        areas = js["BizAreaList"]
        for area in areas:
            if area["id"] > 0:
                area_item["areaId"] = area["id"]
                area_item["cityId"] = cityId
                area_item["name"] = area["name"]
                area_item["subareas"] = area["subareas"]
                area_item["count"] = area["count"]
                yield area_item