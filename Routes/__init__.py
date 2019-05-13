class Route:
    
    def __init__(self):

        pass

    __BaseUrl__ = '/api'

    # 测试路由
    status = __BaseUrl__ + '/status'

    # 用户路由
    login = __BaseUrl__ + '/login'

    register = __BaseUrl__ + '/register'

    # 爬虫路由
    __SpiderUrl__ = __BaseUrl__ + '/spider'
    spider_test = __SpiderUrl__ + '/test'
    spider_shops = __SpiderUrl__ + '/shops'
    spider_file  = __SpiderUrl__ + '/shops/file'
    spider_run = __SpiderUrl__ + '/run'
    spider_list = __SpiderUrl__ + '/list'
    spider_record = __SpiderUrl__ + '/record'