import requests
from logg import *
from pymongo import MongoClient
db = MongoClient().companys.all
from redis import Redis
import traceback
from threading import Thread
r = Redis()
all = 489997
# print(int(all / 90))
for i in range(int(all / 90)):
	r.sadd('ids', i)
def get():
	while True:
		id_ = r.spop('ids').decode()
		try:
			url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=90&cityId=530&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3&_v=0.25726104&x-zp-page-request-id=8742b34247e74a43bc387e3119b10f06-1545037051986-388202'
			url = url.format(int(id_) * 90)
			print(id_)
			print(url)
			res = requests.get(url, headers=get_ua())
			data = res.json()
			print(data['code'])
			if data['code'] == 200:
				for job in data['data']['results']:
					name = job['company']['name']
					url_ = job['company']['url']
					type_ = job['company']['type']['name']
					size = job['company']['size']['name']
					db.insert({
						'name': name,
						'url': url_,
						'type': type_,
						'size': size
					})
					print(name)
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
			d = [i['name'], i['type'], i['url'], i['size']]
			fres.write('\t'.join(d) +'\n')
			ss.add(i['name'])
if __name__ == '__main__':
    run()


