# -*- coding: utf-8 -*-
import config
from flask import Flask,make_response,jsonify,request
from flask_jwt import JWT
from datetime import datetime

app = Flask(__name__)

# 读取config文件
app.config.from_object(config)

# 规定统一的相应格式
def response(data = None, msg ="ok", status = 200):
    response = make_response(jsonify({
        "status":status,
        "data":data,
        "msg":msg
        }), status)

    return response

#日志处理及错误监听
import Exceptions.Log
# 配置JWT
from Services.JwtService import JwtService as JwtS

jwt = JWT(app, JwtS().authenticate, JwtS().identify)


#api的业务逻辑及跨域设置
import Controllers

@app.route('/api/__status')
def status():
    import flask
    return flask.__version__