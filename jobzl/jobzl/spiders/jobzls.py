# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import JobzlItem, JobzlItem2
from scrapy import Request

with open("jobzl/spiders/zhaopin.json", 'r', encoding='utf-8') as load_f:
	load_dict = json.load(load_f)

ids = []
jobtypes = load_dict['basic']['dict']['jobType']
industrys = load_dict['basic']['dict']['industry']
provinces = load_dict['basic']['dict']['location']['province']
industry_is = []
for i in industrys:
	for child in i['sublist']:
		industry_is.append(child['code'])
for i in jobtypes[1:]:
	for child in i['children']:
		for v in child['children']:
			ids.append(v['value'])
citys = []
for i in provinces:
	for child in i['sublist']:
		citys.append(child['code'])


class JobzlsSpider(scrapy.Spider):
	name = 'jobzls'
	allowed_domains = ['zhaopin.com']
	start_urls = []
	for city in citys:
		for i in ids:
			url = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId={}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&jobType={}&kt=3&_v=0.80333302&x-zp-page-request-id=2ed556b61ff449a9bebb989d7707d82c-1545101313233-870251'
			url = url.format(str(city), str(i))
			start_urls.append(url)
	print(len(start_urls))

	def parse(self, response):
		jobtype = re.findall('&jobType=\d+&', response.url)[0]
		base_url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=90&cityId=489&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&jobType={}&kt=3&_v=0.80333302&x-zp-page-request-id=2ed556b61ff449a9bebb989d7707d82c-1545101313233-870251'
		data = json.loads(response.body.decode())
		if data['code'] == 200:
			for i in data['data']['results']:
				item = JobzlItem()
				item['_id'] = i['company']['name']
				item['type_'] = i['company']['type']['name']
				item['size'] = i['company']['size']['name']
				item['hangye'] = ''
				item['zhizhao'] = ''
				# d = dict(
				# 	_id=i['company']['name'],
				# 	type_=i['company']['type']['name'],
				# 	size=i['company']['size']['name'],
				# 	hangye='',
				# 	zhizhao=''
				#     )
				# datas.append(d)
				yield item

		all_num = data['data']['numFound']
		counts = all_num // 90 + 1
		for i in range(1, counts + 1):
			yield Request(url=base_url.format(i * 90, jobtype), callback=self.parse_detail)

	def parse_detail(self, response):
		data = json.loads(response.body.decode())


		if data['code'] == 200:
			for i in data['data']['results']:
				item = JobzlItem()
				item['_id'] = i['company']['name']
				item['type_'] = i['company']['type']['name']
				item['size'] = i['company']['size']['name']
				item['hangye'] = ''
				item['zhizhao'] = ''
				# d = dict(
				# 	_id=i['company']['name'],
				# 	type_=i['company']['type']['name'],
				# 	size=i['company']['size']['name'],
				# 	hangye='',
				# 	zhizhao=''
				#     )
				# datas.append(d)
				yield item
