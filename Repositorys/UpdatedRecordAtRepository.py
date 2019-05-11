from Repositorys.BaseRepository import BaseRepository

class UpdatedRecordRepository(BaseRepository):
    
    def __init__(self):

        super().__init__("updated_record")