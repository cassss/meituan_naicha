import csv,codecs,time,config,logging
from datetime import datetime
from Repositorys.UpdatedRecordAtRepository import UpdatedRecordRepository as Record
#引入你的爬虫
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

class Runer(object):
    
    def __init__(self):
        self.now = datetime.utcnow()
        self.publics = config.PUBLIC_DIR

    def start(self, spider_name):
        res = Record().qurey.create({
            "spider_name":spider_name,
            "start_at":self.now
        })
        update_dict = {"msg":"ok"}
        try:
            runner = CrawlerRunner(get_project_settings())
            deferred = runner.crawl(spider_name)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
        except Exception as e:
            update_dict["msg"] = e.__str__()
        finally:
            end_at = datetime.utcnow()
            update_dict["end_at"] = end_at
            Record().qurey.where({"_id":res.inserted_id}).update(update_dict)
            return True


    # def newShopList(self, file = "newShopList.csv"):        
    #     is_first = True

    #     with open(self.data + file, "w", encoding="utf-8") as f:
    #         wirter = csv.writer(f)
    #         for shop in self.db["new_naicha"].find():
    #             if is_first:
    #                 keys = shop.keys()
    #                 wirter.writerow(keys)
    #                 is_first = False
    #             wirter.writerow(list(shop.values()))

    #     return file

    # def afterUpdateNewShopList(self, file = "afterUpdateNewShopList_%d.csv"%(int(time.time()))):
    #     update = self.db["update_time"]
    #     updated_at = update.find_one({"spider_name":"naicha"}, sort=[('strat_at', -1)])

    #     is_first = True
    #     if updated_at:
    #         with open(self.data + file, "w", encoding="utf-8") as f:
    #             wirter = csv.writer(f)
    #             for shop in self.db["new_naicha"].find({"created_at":{"$gte":updated_at["strat_at"]}}):
    #                 if is_first:
    #                     keys = shop.keys()
    #                     wirter.writerow(keys)
    #                     is_first = False
    #                 wirter.writerow(list(shop.values()))
    #     return file

    # def afterUpdateShopList(self, file = "afterUpdateShopList_%d.csv"%(int(time.time()))):
    #     update = self.db["update_time"]
    #     updated_at = update.find_one({"spider_name":"naicha"}, sort=[('strat_at', -1)])
    #     is_first = True
    #     if updated_at:
    #         with open(self.data + file, "w", encoding="utf-8") as f:
    #             wirter = csv.writer(f)
    #             for shop in self.db["new_naicha"].find({"updated_at":{"$gte":updated_at["strat_at"]}}):
    #                 if is_first:
    #                     keys = shop.keys()
    #                     wirter.writerow(keys)
    #                     is_first = False
    #                 wirter.writerow(list(shop.values()))
    #     return file
    
