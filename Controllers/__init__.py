from App import app
from flask import request,url_for,send_from_directory
import config

# 跨域设置
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

@app.route('/api/public/<filename>')
def getfile(filename):
    directory = config.PUBLIC_DIR  # 假设在当前目录
    print(directory)
    return send_from_directory(directory, filename, as_attachment=True)


from Controllers import AuthController,SpiderController