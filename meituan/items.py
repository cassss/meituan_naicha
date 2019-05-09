# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ShopInfoItem(scrapy.Item):

    shop_id = scrapy.Field()
    template = scrapy.Field()
    imageUrl = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    lowestprice = scrapy.Field()
    avgprice = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    showType = scrapy.Field()
    avgscore = scrapy.Field()
    comments = scrapy.Field()
    historyCouponCount = scrapy.Field()
    backCateName = scrapy.Field()
    areaname = scrapy.Field()
    tag = scrapy.Field()
    cate = scrapy.Field()
    recentScreen = scrapy.Field()
    abstracts = scrapy.Field()
    dangleAbstracts = scrapy.Field()
    titleTags = scrapy.Field()
    iUrl = scrapy.Field()
    deals = scrapy.Field()
    posdescr = scrapy.Field()
    ct_poi = scrapy.Field()
    trace = scrapy.Field()
    landmarkDistance = scrapy.Field()
    hasAds = scrapy.Field()
    adsClickUrl = scrapy.Field()
    adsShowUrl = scrapy.Field()
    distance = scrapy.Field()
    cityId = scrapy.Field()
    city = scrapy.Field()
    full = scrapy.Field()
    update_at = scrapy.Item()
    create_at = scrapy.Item()
    first_feed_at = scrapy.Field()
    phone = scrapy.Field()
    pass

class CityInfoItem(scrapy.Item):
    
    cityId = scrapy.Field()
    name = scrapy.Field()
    pinyin = scrapy.Field()
    acronym = scrapy.Field()
    rank = scrapy.Field()
    firstChar = scrapy.Field()
    update_at = scrapy.Field()
    create_at = scrapy.Field()
    pass

class AreaItem(scrapy.Item):

    areaId = scrapy.Field()
    cityId = scrapy.Field()
    name = scrapy.Field()
    subareas = scrapy.Field()
    count = scrapy.Field()
    update_at = scrapy.Field()
    create_at = scrapy.Field()

class ShopCountItem(scrapy.Item):

    count = scrapy.Field()
    cityId = scrapy.Field()
    update_at = scrapy.Field()
    create_at = scrapy.Field()
    pass

class AreaCountItem(scrapy.Item):

    count = scrapy.Field()
    cityId = scrapy.Field()
    areaId = scrapy.Field()
    update_at = scrapy.Field()
    create_at = scrapy.Field()
    pass