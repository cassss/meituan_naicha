from App import app,response
from Routes import Route
from flask import Flask, jsonify, request, abort
from Repositorys.AuthRepository import AuthRepository
from Services.JwtService import JwtService

Auth = AuthRepository()
Jwts = JwtService()

@app.route(Route.register, methods=['POST'])
def register():
    request_json = request.get_json()
    if not Auth.hasUser(request_json):
        user = __tansToCreate(request_json)
        user = Auth.create(user)
        if user:
            return response("创建成功")
    return response("已存在的用户名或邮箱", 400)

# @app.route(Route.login, methods=['POST'])
# def login():
#     request_json = request.get_json()
#     return JwtService.authenticate(request_json["email"], request_json["password"])

def __tansToCreate(request_json):

    password = Jwts.enPassWord(request_json["password"])

    return {
        "username":request_json["username"],
        "password":password,
        "email":request_json["email"]
    }

    