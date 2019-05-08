# -*- coding: utf-8 -*-
import pymongo,redis
from scrapy.conf import settings

client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])

db = client[settings['MONGO_DB']]  # 获得数据库的句柄
coll = db["area_count"]
shop_ids = []
delCount = 0

i = 0
for shop in coll.find({},{ "areaId": 1, "_id":1}):
    shop_id = shop["areaId"]
    if shop_id in shop_ids:
        coll.delete_one({'_id': shop["_id"]})
        delCount += 1
    else:
        shop_ids.append(shop_id)
    i += 1
    if i % 2000 == 0:
        print(i,delCount)
print(delCount)
