import datetime,os,time

SECRET_KEY = "yuanli"
DEBUG = True

Home_DIR = os.getcwd()
STORGE_DIR = Home_DIR + "/Storge"
LOG_DIR = STORGE_DIR + "/logs"
SCRAPY_LOG = LOG_DIR + "/scrapy/%d.log"%(int(time.time()))
FLASK_LOG = LOG_DIR + "/flask"
PUBLIC_DIR = STORGE_DIR + "/public"
SCRAPY_JOB_DIR=STORGE_DIR + '/pause/%d'%(int(time.time()))

PROXY_STATUS = True
PROXY_SERVER = "http://http-dyn.abuyun.com:9020"
PROXY_USER_PASS = b"HRID47110GXA703D:FDCCBDA2D4F74C45"

MONGO_HOST = "mongo"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "Spider"  # 库名 

REDIS_HOST = "redis"  # 主机IP
REDIS_PORT = 6379 # 端口号
REDIS_DB   = 0 #库名

JWT_AUTH_URL_RULE = "/api/login"
JWT_AUTH_USERNAME_KEY = "email"
JWT_AUTH_HEADER_PREFIX = "Bearer"
JWT_EXPIRATION_DELTA = datetime.timedelta(days = 1)

DEBUG_LOG_FORMAT = (
    '-' * 80 + '\n' +
    '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
    '%(message)s\n' +
    '-' * 80
)

PROD_LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'

