import csv,codecs,time,config
from datetime import datetime
from scrapy import cmdline
from Repositorys.UpdatedRecordAtRepository import UpdatedRecordRepository as Record

class Runer(object):
    
    def __init__(self):
        self.now = datetime.utcnow()
        self.logs = config.LOG_DIR + '/scrapy'
        self.publics = config.PUBLIC_DIR

    def start(self, spider_name = "naicha", has_re = False):
        Record().qurey.create({
            "spider_name":spider_name,
            "start_at":self.now
        })
        log = "--logfile=%s/spider-%s-%s.log"%(self.logs, self.now.strftime("%Y-%m-%d"), spider_name)
        cmdline.execute(['scrapy', 'crawl', spider_name, log])
        if has_re:
            cmdline.execute(['scrapy', 'crawl', "re_"+spider_name, log])

        end_at = datetime.utcnow()

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
    
