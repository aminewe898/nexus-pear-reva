import json
x=json.load(open('work/drc-new.json'))
for v in x['unconnected_items']:print(v['items'])
