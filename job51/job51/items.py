# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class Job51Item(scrapy.Item):
    _id = Field()
    type_ = Field()
    size = Field()
    hangye = Field()
    zhizhao = Field()

class Job51Item2(scrapy.Item):
    _id = Field()



