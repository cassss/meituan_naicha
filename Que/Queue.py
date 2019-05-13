
from Services.RedisService import RedisService
import time,asyncio

class RedisQueue(object):
    def __init__(self, name, namespace='queue'):
        self.__res= RedisService().DB()
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        return self.__res.llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, item):
        return self.__res.rpush(self.key, item)  # 添加新元素到队列最右方

    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.__res.blpop(self.key, timeout=timeout)
        # if item:
        #     item = item[1]  # 返回值为一个tuple
        return item

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__res.lpop(self.key)  
        return item
    
    async def work(self):
        while True:
            res = self.get_nowait()
            if not res:
                await asyncio.sleep(1)                
                continue
            if isinstance(res, bytes):
                res = res.decode()
            print("Queue[%s] strat work!"%(self.key))
            await self.AsyncRun(res)
            print("Queue[%s] work done!"%(self.key))

    # 队列运行的方法，继承后覆盖即可
    async def AsyncRun(self, res):
        return self.run(res)

    # 队列运行的方法，继承后覆盖即可
    def run(self, res):
        return True