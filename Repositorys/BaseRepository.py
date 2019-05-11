from Models.model import ModelBuilder
from bson.objectid import ObjectId

class BaseRepository(object):

    def __init__(self, table):
        self.qurey = ModelBuilder(table)
    
    def create(self, data):
        return self.qurey.create(data)

    def firstById(self, model_id):
        if isinstance(model_id, str):
            model_id = ObjectId(model_id)
        return self.qurey.where({"_id":model_id}).first()

    def updateOneOrCreate(self, data, find = {}):
        self.qurey.updateOneOrCreate(data, find)

    def gen(self, select = None):
        
        return self.qurey.select(select).getGen()
    