# -*- coding: utf-8 -*-
import scrapy
from ..config import *
import re
from scrapy import Request
from ..items import *
from bs4 import BeautifulSoup
import traceback
from scrapy_redis.spiders import RedisCrawlSpider

class JobsSpider(scrapy.Spider):
	name = 'jobs'
	# redis_key = "51job:strat_urls"
	allowed_domains = ['51job.com']
	start_urls = []
	for k1 in citys:
		for k, v in jobs.items():
			url = 'https://search.51job.com/list/{},000000,{},00,9,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
			url = url.format(str(k1), str(k))
			start_urls.append(url)

	def parse(self, response):
		# urls = re.findall(b'title="(.+?)" href="(https://jobs\.51job\.com/\w+/\w+\.html)">',
		#                   response.body)
		urls = response.xpath('//span[@class="t2"]/a/@href').extract()
		print(urls)
		for url in urls:
			item = Job51Item2()
			item['_id'] = url
			yield item
		next_url = response.xpath('//a[@id="rtNext"]/@href').extract()
		if next_url != []:
			yield Request(url=next_url[0], callback=self.parse)


	def parse_detail(self, response):
		item = Job51Item()
		# response.encoding = 'gb2312'
		try:
			# response.xpath('//h1/@title').extract_first()
			item['_id'] = response.xpath('//h1/@title').extract_first()
			print(item['_id'])
			types = response.xpath('//p[@class="ltype"]/@title').extract_first().split('|')
			if len(types) != 1:
				item['type_'] = types[0]
				item['size'] = types[1]
				item['hangye'] = types[-1]
			else:
				item['type_'] = ''
				item['size'] = ''
				item['hangye'] = types[0]
			try:
				item['zhizhao'] = response.xpath('//span[@class="icon_det"]/@title').extract_first()
			except:
				item['zhizhao'] = ''

			yield item
		except:
			print(traceback.format_exc())
			print(response.url)
			print(response.body.decode('gb2312'))
