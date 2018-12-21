# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class JobzlItem(scrapy.Item):
	_id = Field()
	type_ = Field()
	size = Field()
	hangye = Field()
	zhizhao = Field()
class JobzlItem2(scrapy.Item):
	data = Field()
