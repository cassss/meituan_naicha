# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings

client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])

db = client[settings['MONGO_DB']]  # 获得数据库的句柄
coll = db["shop_url"]
shop_ids = []
delCount = 0

for shop in coll.find({},{ "poiid": 1, "_id":1}):
    shop_id = shop["poiid"]
    if shop_id in shop_ids:
        coll.delete_one({'_id': shop["_id"]})
        delCount += 1
    else:
        shop_ids.append(shop_id)
    if delCount % 1000 == 0:
        print(delCount)

print(delCount)
