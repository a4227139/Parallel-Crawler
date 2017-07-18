# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    addr = scrapy.Field()
    area=scrapy.Field()
    link=scrapy.Field()
    tag=scrapy.Field()
    pass
class OldItem(scrapy.Item):
    name = scrapy.Field()
    area = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    type = scrapy.Field()
    acreage = scrapy.Field()
    build_in = scrapy.Field()
    addr = scrapy.Field()
    link = scrapy.Field()