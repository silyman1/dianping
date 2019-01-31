# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #店名
    shop = scrapy.Field()
    #行政区
    district = scrapy.Field()
    #街道
    street = scrapy.Field()
    #评论数
    comments_count = scrapy.Field()
    #评论数大于100
    is_more_than_100 = scrapy.Field()
	#均价
	price = scrapy.Field()
    #菜系
    foodtype = scrapy.Field()
    #星级
    star_level = scrapy.Field()
    #口味
    flavour = scrapy.Field()
    #环境
    environment = scrapy.Field()
    #服务
    service = scrapy.Field()
    #经度
    longitude = scrapy.Field()
    #纬度
    latitude = scrapy.Field()
    #综合评分
    overall_score = scrapy.Field()