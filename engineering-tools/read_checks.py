import json,collections
for fn in ['erc-new','drc-new']:
 d=json.load(open('work/'+fn+'.json'));print(fn,d.keys())
 if fn.startswith('erc'):
  for sh in d.get('sheets',[]):
   for v in sh.get('violations',[]):print(v['description'],v.get('items'))
 else:
  print(collections.Counter(v['type'] for v in d['violations']))
  for v in d['violations']:
   if v['type'] not in ['silk_over_copper','silk_overlap','silk_edge_clearance']:print(v['type'],v['description'],v.get('items'))
