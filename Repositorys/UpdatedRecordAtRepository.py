from Repositorys.BaseRepository import BaseRepository

class UpdatedRecordRepository(BaseRepository):
    
    def __init__(self):

        super().__init__("updated_record")
    
    def isRuning(self, name):
        res = self.qurey.where({"spider_name":name, "end_at":None}).first()
        if res:
            return True
        else:
            return False