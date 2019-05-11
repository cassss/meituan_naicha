from Repositorys.BaseRepository import BaseRepository

class CityRepository(BaseRepository):
    
    def __init__(self):

        super().__init__("city_info")

    def allCitys(self, limit, offset):
        return self.qurey.pagenate(True, limit, offset, "cityId", 1)