import json
for v in json.load(open('work/drc-new.json'))['violations']:print(v['type'],v['items'])
