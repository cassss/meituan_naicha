import jwt,time,datetime,config
from App import response
from werkzeug.security import generate_password_hash,check_password_hash
from Repositorys.AuthRepository import AuthRepository as Auth
from Exceptions.ApiException import ApiException

class JwtService(object):

    def __init__(self):
        self.auth = Auth()
    #哈希加盐的密码加密方法
    def enPassWord(self, password):#将明密码转化为hash码
        return generate_password_hash(password)#返回转换的hash码

    def checkPassWord(self, enpassword,password):#第一参数是从数据查询出来的hash值，第二参数是需要检验的密码
        return check_password_hash(enpassword,password)#如果匹配返回true

    def encode_auth_token(self, user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return False

    def authenticate(self, email, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        
        userInfo = self.auth.findByEmail(email)
        if (userInfo is None):
            raise ApiException("用户不存在", 404)
        else:
            if (self.checkPassWord(userInfo.password, password)):
                userId = userInfo._id
                login_time = int(time.time())
                self.auth.updateLoginTimeById(userId, login_time)  
                token = self.encode_auth_token(str(userId), login_time)
                if token:
                    userInfo.id = str(userId)
                    return userInfo
            else:
                raise ApiException("认证失败", 404)

    def identify(self, payload):
        """
        用户鉴权
        :return: list
        """
        _id = payload['identity']
        user = self.auth.firstById(_id)
        return user
