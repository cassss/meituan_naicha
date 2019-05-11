import redis,config

class RedisService(object):

    def __init__(self):
        pass

    def DB(self):
        return redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)
