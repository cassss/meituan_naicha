import pymongo,csv,codecs
from datetime import datetime
from scrapy.conf import settings
from scrapy import cmdline

class SpiderRuner(object):
    
    def __init__(self):
        self.now = datetime.utcnow()
        client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        self.db = client[settings['MONGO_DB']]  # 获得数据库的句柄

    def start(self, spider_name = "naicha"):
        print("开始查询，开始时间为:%s"%(str(self.now)))
        update = self.db["update_time"]
        update.insert({
            "spider_name":spider_name,
            "strat_at":self.now
        })
        log = "--logfile=logs/spider-%s-%s.log"%(str(self.now), spider_name)
        cmdline.execute(['scrapy', 'crawl', spider_name, log])
        cmdline.execute(['scrapy', 'crawl', "re_"+spider_name, log])

        end_at = datetime.utcnow()
        print("Spider work finish at %s"%(str(end_at)))

    def newShopList(self, file = "data/newShopList.csv"):        
        is_first = True

        with open(file, "w", encoding="utf-8") as f:
            wirter = csv.writer(f)
            for shop in self.db["new_naicha"].find():
                if is_first:
                    keys = shop.keys()
                    wirter.writerow(keys)
                    is_first = False
                wirter.writerow(list(shop.values()))
    
    def afterUpdateShopList(self, file = "data/afterUpdateShopList.csv"):
        update = self.db["update_time"]
        updated_at = update.find_one({"spider_name":"naicha"}, sort=[('strat_at', -1)])

        is_first = True
        if updated_at:
            with open(file, "w", encoding="utf-8") as f:
                wirter = csv.writer(f)
                for shop in self.db["new_naicha"].find({"created_at":{"$gte":updated_at["strat_at"]}}):
                    if is_first:
                        keys = shop.keys()
                        wirter.writerow(keys)
                        is_first = False
                    wirter.writerow(list(shop.values()))
                    

def main():
    spider = SpiderRuner()
    spider.start()

if __name__ == "__main__":
    main()
    
