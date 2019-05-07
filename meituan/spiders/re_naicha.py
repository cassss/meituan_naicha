# -*- coding: utf-8 -*-
import scrapy,random,time,json,redis,math,re
from scrapy import Request
from meituan.items import ShopInfoItem
from scrapy.conf import settings

class ReNaiChaSpider(scrapy.Spider):
    name = 're_naicha'
    
    serach_url = "https://apimobile.meituan.com/group/v4/poi/pcsearch/%d?uuid=%s&userid=-1&limit=32&offset=%d&cateId=21329"

    def start_requests(self):
        # client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # db = client[settings['MONGO_DB']]  # 获得数据库的句柄
        # coll = db["city_info"]
        
        # for city in coll.find({},{ "cityId": 1}):
        #     city_id = city["cityId"]
        rds = redis.Redis(host='localhost', port=6379, decode_responses=True)
        urls = rds.lrange("err_url", 0, -1)
        self.shop_ids = rds.lrange("shop_ids", 0, -1)
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        shop_item = ShopInfoItem()
        res = response.body.decode()
        js = json.loads(res)
        searchResult = js["data"]["searchResult"]
        count = int(js["data"]["totalCount"])
        
        for shop in searchResult:
            if shop["id"] not in self.shop_ids:
                shop_item["shop_id"] = shop["id"]
                shop_item["template"] = shop["template"]
                shop_item["imageUrl"] = shop["imageUrl"]
                shop_item["title"] = shop["title"]
                shop_item["address"] = shop["address"]
                shop_item["lowestprice"] = shop["lowestprice"]
                shop_item["avgprice"] = shop["avgprice"]
                shop_item["latitude"] = shop["latitude"]
                shop_item["longitude"] = shop["longitude"]
                shop_item["showType"] = shop["showType"]
                shop_item["avgscore"] = shop["avgscore"]
                shop_item["comments"] = shop["comments"]
                shop_item["historyCouponCount"] = shop["historyCouponCount"]
                shop_item["backCateName"] = shop["backCateName"]
                shop_item["areaname"] = shop["areaname"]
                shop_item["tag"] = shop["tag"]
                shop_item["cate"] = shop["cate"]
                shop_item["recentScreen"] = shop["recentScreen"]
                shop_item["abstracts"] = shop["abstracts"]
                shop_item["dangleAbstracts"] = shop["dangleAbstracts"]
                shop_item["titleTags"] = shop["titleTags"]
                shop_item["iUrl"] = shop["iUrl"]
                shop_item["deals"] = shop["deals"]
                shop_item["posdescr"] = shop["posdescr"]
                shop_item["ct_poi"] = shop["ct_poi"]
                shop_item["trace"] = shop["trace"]
                shop_item["landmarkDistance"] = shop["landmarkDistance"] 
                shop_item["hasAds"] = shop["hasAds"]
                shop_item["adsClickUrl"] = shop["adsClickUrl"]
                shop_item["adsShowUrl"] = shop["adsShowUrl"]
                shop_item["distance"] = shop["distance"]
                shop_item["cityId"] = shop["cityId"]
                shop_item["city"] = shop["city"]
                shop_item["full"] = shop["full"]
                yield shop_item

        offset = re.search(r'offset=([0-9]+)&', response.url).group(1)
        city_id = re.search(r'/pcsearch/([0-9]+)?', response.url).group(1)
        next_offset = int(offset) + 32
        if count >= next_offset:
            yield Request(self.serach_url%(int(city_id), self._getUUId(), next_offset), callback=self.parse, dont_filter= True)
    
    def _getUUId(self):
        return "%s.%d.1.0.0"%(self._ranstr(20), int(time.time()))

    def _ranstr(self, num):
        H = 'abcdefghijklmnopqrstuvwxyz'
        salt = ''
        for i in range(num):
            salt += random.choice(H)

        return salt