from Que.Queue import RedisQueue
from Services.RunerServices import Runer

class Queue(RedisQueue):
    def __init__(self):
        super().__init__("test")

    def run(self, res):
        print(res)
