from Que.Queue import RedisQueue
from Services import RunerService

class Queue(RedisQueue):
    def __init__(self):
        super().__init__("spider")

    def run(self, res):
        service = RunerService.Runer()
        res = service.start(res)
        del service
        return res