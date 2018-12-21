from redis import Redis

r = Redis(host='127.0.0.1')
from config import *

start_urls = []
for k1 in citys:
	for k, v in jobs.items():
		url = 'https://search.51job.com/list/{},000000,{},00,9,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
		url = url.format(str(k1), str(k))
		r.sadd('51job:strat_urls', url)
