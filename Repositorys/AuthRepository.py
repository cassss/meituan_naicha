from Repositorys.BaseRepository import BaseRepository

class AuthRepository(BaseRepository):
    
    def __init__(self):

        super().__init__("users")

    def hasUser(self, username, email):
        
        return self.qurey.whereOr([
            {"username":username},
            {"email":email}
        ]).count()

    def findByEmail(self, email):
        
        return self.qurey.where({"email":email}).first()

    def updateLoginTimeById(self, _id, login_time):
        
        return self.qurey.where({"_id":_id}).update({"login_time": login_time})