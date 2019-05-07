# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo,time
from scrapy.conf import settings

class MeituanPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        # self.got_poi = self.r.lrange("got_poi", 0, -1)
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄

    def process_item(self, item, spider):
        Item = dict(item)
        now = int(time.time())
        Item["updated_at"] = now

        if spider.name == "naicha" or spider.name == "re_naicha":
            coll = self.db["naicha_data"]  # 获得collection的句柄
            Item["created_at"] = now
            coll.insert(Item)

        if spider.name == "city":
            coll = self.db["city_info"]
            Item["created_at"] = now
            coll.insert(Item)

        if spider.name == "shop_count":
            coll = self.db["shop_count"]
            Item["created_at"] = now
            coll.insert(Item)

        if spider.name == "update_count":
            coll = self.db["shop_count"]
            cityId = Item["cityId"]
            coll.update_one({"cityId":cityId}, {'$set': Item})
            print(cityId, Item["count"])
        return item
