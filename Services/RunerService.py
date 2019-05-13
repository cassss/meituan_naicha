import csv,codecs,time,config,logging,os
from datetime import datetime
from Repositorys.UpdatedRecordAtRepository import UpdatedRecordRepository as Record

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
            os.system("scrapy crawl %s"%(spider_name))
        except Exception as e:
            update_dict["msg"] = e.__str__()
            print(e.__str__())
        finally:
            end_at = datetime.utcnow()
            update_dict["end_at"] = end_at
            Record().qurey.where({"_id":res.inserted_id}).update(update_dict)
            return True