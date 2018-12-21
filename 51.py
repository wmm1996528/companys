import requests
from logg import *
from pymongo import MongoClient

coll = MongoClient().companys
db = coll.job512
recent = db.job51
from redis import Redis
import traceback
from threading import Thread
from bs4 import BeautifulSoup

r = Redis()
import re

all = 489997
# print(int(all / 90))
for i in range(1, 2001):
	r.sadd('id51', i)


def get():
	while True:
		id_ = r.spop('id51').decode()
		try:
			url = 'https://search.51job.com/list/010000,000000,0000,{},9,99,%2B,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
			url = url.format(int(id_))
			print(id_)
			print(url)
			res = requests.get(url, headers=get_ua())
			res.encoding = 'gb2312'
			urls = re.findall('title="(.+?)" href="(https://jobs\.51job\.com/all/\w+\.html)">', res.text)
			print(urls)
			for i in urls:
				name, url = i
				db.insert({
					'name': name,
					'url': url,
				})
			r.sadd('old', url)
		except:
			print(traceback.format_exc())
			r.sadd('ids', id_)


def run():
	ths = []
	for i in range(10):
		t = Thread(target=get, args=())
		ths.append(t)
	for i in range(10):
		ths[i].start()
	for i in range(10):
		ths[i].join()


def daochu():
	ss = set()
	fres = open('res.txt', 'w', encoding='utf-8')
	for i in db.find():
		if i['name'] not in ss:
			d = [strips(i['name']), strips(i['type_']), strips(i['hangye']), strips(i['size']),strips(i['zhizhao_name'].replace('营业执照：', ''))]
			fres.write('\t'.join(d) + '\n')
			ss.add(i['name'])


# for i in recent.find():
# 	r.sadd('id512', i['url'])

def erci():
	while True:
		url = r.spop('id512')
		try:
			res = requests.get(url, headers=get_ua())
			res.encoding = 'gb2312'
			soup = BeautifulSoup(res.text, 'lxml')
			name = soup.find('h1').get_text()
			types = soup.find('p', {'class': 'ltype'}).get_text().split('|')
			if len(types) != 1:
				type_ = types[0]
				size = types[1]
				hangye = types[-1]
			else:
				type_ = ''
				size = ''
				hangye = types[0]
			try:
				zhizhao_name = soup.find('span', {'class': 'icon_det'}).get_text()
			except:
				zhizhao_name = ''
			data = {
				'name': name,
				'type_': type_,
				'size': size,
				'hangye': hangye,
				'zhizhao_name': zhizhao_name,
			}
			print(name)
			db.insert(data)
		except:
			print(traceback.format_exc())
			print(url)
			r.sadd('id512', url)


def run2():
	ths = []
	for i in range(10):
		t = Thread(target=erci, args=())
		ths.append(t)
	for i in range(10):
		ths[i].start()
	for i in range(10):
		ths[i].join()


if __name__ == '__main__':
	# run2()
	daochu()
