import json
with open("zhaopin.json", 'r', encoding='utf-8') as load_f:
	load_dict = json.load(load_f)
ids = []
jobtypes = load_dict['basic']['dict']['jobType']
for i in jobtypes[1:]:
	for child in i['children']:
		for v in child['children']:
			ids.append(v['value'])
print(len(ids))