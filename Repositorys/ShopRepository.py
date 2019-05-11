from Repositorys.BaseRepository import BaseRepository

class ShopRepository(BaseRepository):
    
    def __init__(self):

        super().__init__("new_naicha")

    def allShop(self, limit, offset):
        return self.qurey.pagenate(True, limit, offset, "first_feed_at", -1)