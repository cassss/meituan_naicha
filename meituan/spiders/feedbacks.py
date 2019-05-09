# -*- coding: utf-8 -*-
import scrapy,pymongo,re
from scrapy import Request
from meituan.items import ShopInfoItem
from scrapy.conf import settings

class FeedBackpider(scrapy.Spider):
    name = 'feedbacks'
    
    serach_url = "https://i.meituan.com/poi/%d/feedbacks/page_%d"

    def start_requests(self):
        client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        db = client[settings['MONGO_DB']]  # 获得数据库的句柄
        coll = db["new_naicha"]
        has_city = []
        for shop in coll.find({},{ "shop_id": 1}):
            shop_id = shop["shop_id"]
            yield Request(self.serach_url%(shop_id, 1), callback=self.parse)

    def parse(self, response):
        shop_id = re.search(r"poi/([0-9]+)/feedbacks", response.url).group(1)
        shop_id = int(shop_id)
        next_page_num = response.xpath('//div[@class="pager"]//a[@gaevent="imt/deal/feedbacklist/pageNext"]/@data-page-num').extract()
        if next_page_num:
            next_page_num = next_page_num[0]
            yield Request(self.serach_url%(int(shop_id), int(next_page_num)), callback=self.parse)
        else:
            feed_item = ShopInfoItem()
            time = response.xpath('//dd[@class="dd-padding"][last()]//div[@class="user-info-text"]//weak[@class="time"]/text()').extract()
            if time:
                feed_item["first_feed_at"] = time[0]
            else:
                feed_item["first_feed_at"] = "No Feed"
            feed_item["shop_id"] = shop_id
            yield feed_item