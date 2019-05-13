from datetime import datetime
from App import app,response
from Exceptions.ApiException import ApiException
import logging,config


loghandler = logging.FileHandler("%s/flask-%s.log"%(config.FLASK_LOG, datetime.now().strftime("%Y-%m-%d")))
loghandler.setLevel(logging.INFO)
logging_format = logging.Formatter(
        '[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s')
loghandler.setFormatter(logging_format)
app.logger.addHandler(loghandler)

# 错误监听
@app.errorhandler(Exception)
def handle_Exception(error):
    msg = "服务器错误"
    status = 500
    if isinstance(error, ApiException):
        msg = error.message
        status = error.status
    elif config.DEBUG:
        msg = error.__str__()
    app.logger.error(msg)
    return response(msg = msg, status = status)

