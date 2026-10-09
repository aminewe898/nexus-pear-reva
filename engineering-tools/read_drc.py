import json,collections
x=json.load(open('work/drc-new.json'));print(collections.Counter(v['type'] for v in x['violations']))
for v in x['violations']:
 if v['type'] not in ['silk_over_copper','silk_overlap','silk_edge_clearance']:print(v['type'],v['description'],[a['description'] for a in v['items']])
