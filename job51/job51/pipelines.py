# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import pymongo
from .settings import MONGODB_HOST


class Job51Pipeline(object):
	db = MongoClient(host=MONGODB_HOST).companys.job51only

	def process_item(self, item, spider):
		data = dict(item)
		try:
			self.db.insert(data)
		except pymongo.errors.DuplicateKeyError:
			pass
		return item
