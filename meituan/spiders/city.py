# -*- coding: utf-8 -*-
import scrapy,random,time,json,re
from scrapy import Request
from meituan.items import CityInfoItem

class CitySpider(scrapy.Spider):
    name = 'city'
    
    def start_requests(self):
        start_url = "https://www.meituan.com/changecity/"
        yield Request(start_url, callback=self.parse )

    def parse(self, response):
        cityitem = CityInfoItem()
        js = response.xpath('//*[@id="main"]/script[3]/text()').extract()[0]
        jsons = re.search(r'"openCityList":(\[.*?\}\]\]\]),', js).group(1)
        jsons = str(jsons)
        jsons = json.loads(jsons)
        for i in range(0, len(jsons)):
            for j in range(0, len(jsons[i][1])):
                cityitem["cityId"] = jsons[i][1][j]["id"]
                cityitem["name"] = jsons[i][1][j]["name"]
                cityitem["pinyin"] = jsons[i][1][j]["pinyin"]
                cityitem["acronym"] = jsons[i][1][j]["acronym"]
                cityitem["rank"] = jsons[i][1][j]["rank"]
                cityitem["firstChar"] = jsons[i][1][j]["firstChar"]

                yield cityitem


            