import re,json,pathlib
root=pathlib.Path(r'C:\Program Files\KiCad\10.0\share\kicad')
def tokens(s): return re.findall(r'"(?:\\.|[^"\\])*"|[^\s()]+|[()]',s)
def parse(s):
 t=iter(tokens(s))
 def expr(x):
  if x=='(':
   a=[]
   for y in t:
    if y==')': return a
    a.append(expr(y))
  return json.loads(x) if x.startswith('"') else x
 return expr(next(t))
def walk(x,key):
 if isinstance(x,list):
  if x and x[0]==key: yield x
  for a in x: yield from walk(a,key)
def child(x,k):return next((a for a in x if isinstance(a,list) and a and a[0]==k),None)
if __name__=='__main__':
 a=parse((root/'symbols/RF_Module.kicad_sym').read_text(encoding='utf8'))
 s=next(x for x in a if isinstance(x,list) and x[:2]==['symbol','ESP32-S3-WROOM-1'])
 for p in walk(s,'pin'):print(child(p,'number')[1],child(p,'name')[1],p[1])
