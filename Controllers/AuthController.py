from App import app,response
from Routes import Route
from flask import Flask, jsonify, request, abort
from Repositorys.AuthRepository import AuthRepository
from Services.JwtService import JwtService
from Exceptions.Log import ApiException

@app.route(Route.register, methods=['POST'])
def register():
    Auth = AuthRepository()
    request_json = request.get_json()
    username = request_json["username"]
    email = request_json["email"]
    check = Auth.hasUser(username, email)
    if not check:
        user = __tansToCreate(request_json)
        user = Auth.create(user)
        if user:
            return response("创建成功")
    
    raise ApiException("创建失败，已存在用户%s,request:%s"%(check, request_json))

# @app.route(Route.login, methods=['POST'])
# def login():
#     request_json = request.get_json()
#     return JwtService.authenticate(request_json["email"], request_json["password"])

def __tansToCreate(request_json):
    Jwts = JwtService()

    password = Jwts.enPassWord(request_json["password"])
    return {
        "username":request_json["username"],
        "password":password,
        "email":request_json["email"]
    }

    