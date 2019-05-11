# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from datetime import datetime
from Repositorys.ShopRepository import ShopRepository as Shop
from Repositorys.CityRepository import CityRepository as City
from Repositorys.AreaRepository import AreaRepository as Area

class MeituanPipeline(object):

    def process_item(self, item, spider):
        Item = dict(item)

        if spider.name == "naicha" or spider.name == "feedbacks":
            Shop().updateOneOrCreate(Item, {"shop_id":Item["shop_id"]})

        if spider.name == "city":
            City().updateOneOrCreate(Item, {"cityId":Item["cityId"]})

        if spider.name == "area":
            Area().updateOneOrCreate(Item, {"areaId":Item["areaId"]})

        return item
