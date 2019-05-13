from App import app,response
from Routes import Route
from flask import Flask, jsonify, request, abort
from flask_jwt import jwt_required, current_identity
from Repositorys.ShopRepository import ShopRepository
from Repositorys.UpdatedRecordAtRepository import UpdatedRecordRepository as Record
from Services.RunerService import Runer
from Que.Spider import RedisQueue

Shop = ShopRepository()

@app.route(Route.spider_test)
@jwt_required()
def test():
    return response(current_identity.username)

@app.route(Route.spider_shops)
@jwt_required()
def index():
    request_all = request.values
    limit = request_all.get("limit", type=int, default= 20)
    offset = request_all.get("offset", type=int, default= 0)
    res = Shop.allShop(limit, offset)

    return response(res)

@app.route(Route.spider_list)
@jwt_required()
def spider_list():
    spiders = [
        "naicha",
        "city",
        "feedbacks"
    ]

    return response(spiders)

@app.route(Route.spider_run, methods=['POST'])
@jwt_required()
def run():
    request_all = request.get_json()
    spider_name = request_all["spider_name"]
    queue_name = request_all["queue_name"]
    reasion = "正在运行中"
    if not Record().isRuning(spider_name):
        q = RedisQueue(queue_name)
        if q.put(spider_name):
            return response("爬虫已进入队列,爬虫名为：%s"%(spider_name))
        reasion = "进入队列失败"
    return response("爬虫进入队列失败,爬虫名为：%s, 原因:%s"%(spider_name, reasion))