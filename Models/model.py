import pymongo,config
from datetime import datetime

class Model(object):
    
    def __init__(self, table, data):
 
        self.table = table
        self.data = data
        self.hidden = []

    def __getattr__(self, attr):
        if (attr not in self.hidden) and (attr not in self.data):
            return None
        return self.data[attr]

    
    def save():

        self.updated_at = datetime.utcnow()
        return self.table.update_one({"_id":self._id}, self.__dict__())
        



class ModelBuilder(object):

    def __init__(self, table):
        client = pymongo.MongoClient(host=config.MONGO_HOST, port=config.MONGO_PORT)
        db = client[config.MONGO_DB]  # 获得数据库的句柄

        self.table = db[table]

        self.find_roule = {}
        self.select_roule = None

    def select(self, datas):

        select_roule = self.select_roule

        if not select_roule:
            select_roule = {}
        if isinstance(datas,list):
            for data in datas:
                select_roule[data] = 1
        else:
            return self
        
        self.select_roule = select_roule

        return self

    def where(self, datas):
        find_roule = self.find_roule

        if isinstance(datas,list):
            for data in datas:
                find_roule.update(data)
        elif isinstance(datas,dict):
            find_roule.update(datas)
        else:
            return self
        
        self.find_roule = find_roule

        return self

    def whereOr(self, datas):

        find_roule = self.find_roule

        if "$or" not in find_roule:
            find_roule["$or"] = []
        if isinstance(datas,list):
            for data in datas:
                find_roule["$or"].append(data)
        elif isinstance(datas,dict):
            find_roule["$or"].append(datas)
        else:
            return self

        self.find_roule = find_roule
        return self

    def create(self,data):
        now = datetime.utcnow()
        data["updated_at"] = now
        data["created_at"] = now
        return self.table.insert_one(data)

    def update(self, data):
        data["updated_at"] = datetime.utcnow()
        return self.table.update_many(self.find_roule, {
            "$set":data
        })

    def updateOneOrCreate(self, data, find = {}):
        now = datetime.utcnow()
        data["updated_at"] = now
        result = self.table.update_one(find,{"$set":data}, True)
        if result.matched_count == 0:
            find.update({"created_at":None})
            self.table.update_many(find,{"$set":{"created_at":now}})
    
    def __end__(self, sort = "_id", sort_type = 1):
        return self.table.find(self.find_roule, self.select_roule).sort(sort, sort_type)

    def get(self,need_dict=False, sort = "_id", sort_type = 1):
        
        models = self.__end__(sort, sort_type)
        model_list = []
        if models:
            for model in models:
                if need_dict:
                    model["_id"] = str(model["_id"])
                    model_list.append(model)
                else:
                    model_list.append(Model(self.table, model))

        return model_list

    def pagenate(self,need_dict=False ,limit = None, offset = None, sort = "_id", sort_type = 1):
        
        models = self.__end__(sort, sort_type)
        count = models.count()
        if limit:
            models = models.limit(limit)
        
        if offset:
            models = models.skip(offset)

        model_list = []
        if models:
            for model in models:
                if need_dict:
                    model["_id"] = str(model["_id"])
                    model_list.append(model)
                else:
                    model_list.append(Model(self.table, model))

        return {
            'count':count,
            'limit':limit,
            'offset':offset,
            'data':model_list
        }

    def count(self):

        return self.__end__().count()

    def first(self):
        
        res = self.table.find_one(self.find_roule, self.select_roule)
        if res:
            return Model(self.table, res)
        else:
            return None

    def getGen(self):
        return self.__end__()