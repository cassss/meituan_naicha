# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random,base64,redis
from scrapy.conf import settings


class MeituanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MeituanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class MyUserAgentMiddleware(UserAgentMiddleware):

    user_agents = settings["USER_AGENTS"]
    cookies = settings["COOKIES"]

    def process_request(self, request, spider):

        request.headers['User-Agent'] = random.choice(self.user_agents)
        request.headers['Cookie'] = self.cookies
        print(request.headers)

class ProxyMiddleware(object): 
    errlist = []

    def process_request(self, request, spider):
        proxyStatus = settings["PROXY_STATUS"]
        if proxyStatus:
            proxyServer = settings["PROXY_SERVER"]
            proxy_user_pass = settings["PROXY_USER_PASS"]
            encoded_user_pass = base64.b64encode(proxy_user_pass)
            request.meta["proxy"] = proxyServer
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass.decode()

    def process_response(self, request, response, spider):
        if response.status == 403:
            return request

        if response.status in [300, 301, 302]:
            if "redirect_urls" in request.meta:
                redirect_url = request.meta['redirect_urls'][0]
                request = request.replace(url=redirect_url)
                return request
            else:
                return response

    def process_exception(self, request, exception, spider):
        name = spider.name
        if request.url in self.errlist:
            return request
        else:
            self.errlist.append(request.url)
            rds = redis.Redis(host='localhost', port=6379, decode_responses=True)
            rds.lpush("err_url", request.url)
        print("\n出现异常:{0}\n".format(str(exception.args[0])))
