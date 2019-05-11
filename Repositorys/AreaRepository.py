from Repositorys.BaseRepository import BaseRepository

class AreaRepository(BaseRepository):
    
    def __init__(self):
        super().__init__("area_info")

    def allAreas(self, limit, offset):
        return self.qurey.pagenate(True, limit, offset, "areaId", -1)