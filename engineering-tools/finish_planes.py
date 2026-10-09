import pcbnew as p,json,math
from pathlib import Path
path=Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path))
def pt(v):return tuple(p.ToMM(v))
def xy(q):return p.VECTOR2I(p.FromMM(q[0]),p.FromMM(q[1]))
def ds(q,a,c):
 dx=c[0]-a[0];dy=c[1]-a[1];n=dx*dx+dy*dy;t=0 if n==0 else max(0,min(1,((q[0]-a[0])*dx+(q[1]-a[1])*dy)/n));return math.hypot(q[0]-a[0]-t*dx,q[1]-a[1]-t*dy)
def orient(a,c,q):return (c[0]-a[0])*(q[1]-a[1])-(c[1]-a[1])*(q[0]-a[0])
def sd(a,c,x,y):
 if orient(a,c,x)*orient(a,c,y)<0 and orient(x,y,a)*orient(x,y,c)<0:return 0
 return min(ds(a,x,y),ds(c,x,y),ds(x,a,c),ds(y,a,c))
pads=[a for f in b.GetFootprints() for a in f.Pads()]
def clear(a,q,net,layer):
 for t in b.GetTracks():
  via=isinstance(t,p.PCB_VIA)
  if via and math.dist(q,pt(t.GetPosition()))<.65:return False
  if t.GetNetCode()==net:continue
  if via:r=p.ToMM(t.GetWidth(p.F_Cu))/2;x=y=pt(t.GetPosition())
  else:r=p.ToMM(t.GetWidth())/2;x=pt(t.GetStart());y=pt(t.GetEnd())
  # Via crosses all layers; stub only its layer.
  if ds(q,x,y)<.3+.2+r+.01:return False
  if (via or t.GetLayer()==layer) and sd(a,q,x,y)<.1+.2+r+.01:return False
 for pad in pads:
  hole=p.ToMM(pad.GetDrillSize().x)
  if hole and math.dist(q,pt(pad.GetPosition()))<hole/2+.15+.25+.01:return False
  if pad.GetNetCode()==net:continue
  box=pad.GetBoundingBox();l=p.ToMM(box.GetLeft());r=p.ToMM(box.GetRight());t=p.ToMM(box.GetTop());d=p.ToMM(box.GetBottom())
  vd=math.hypot(max(l-q[0],0,q[0]-r),max(t-q[1],0,q[1]-d))
  if vd<.515:return False
  if pad.IsOnLayer(layer):
   corners=[(l,t),(r,t),(r,d),(l,d)]
   if l<a[0]<r and t<a[1]<d:return False
   if min(sd(a,q,corners[i],corners[(i+1)%4]) for i in range(4))<.31:return False
 return True
items={str(a.m_Uuid.AsString()):a for a in list(b.GetTracks())+pads}
report=json.load(open('outputs/nexus-pear-reva/validation/drc-stitched.json'))
offsets=sorted([(i*.25,k*.25) for i in range(-12,13) for k in range(-12,13)],key=lambda z:math.hypot(*z))
seen=set();added=0
for violation in report['unconnected_items']:
 for it in violation['items']:
  uid=it['uuid']
  if uid in seen:continue
  seen.add(uid);item=items.get(uid)
  if item is None:continue
  if isinstance(item,p.PCB_TRACK):
   x=pt(item.GetStart());y=pt(item.GetEnd());anchors=[((x[0]+y[0])/2,(x[1]+y[1])/2),x,y];layer=item.GetLayer()
  else:anchors=[pt(item.GetPosition())];layer=p.F_Cu
  net=item.GetNetCode();done=False
  for a in anchors:
   for dx,dy in offsets:
    q=(a[0]+dx,a[1]+dy)
    if not clear(a,q,net,layer):continue
    v=p.PCB_VIA(b);v.SetPosition(xy(q));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(net);b.Add(v)
    if math.dist(a,q)>.001:
     tr=p.PCB_TRACK(b);tr.SetStart(xy(a));tr.SetEnd(xy(q));tr.SetWidth(p.FromMM(.2));tr.SetLayer(layer);tr.SetNetCode(net);b.Add(tr)
    added+=1;print(item.GetNetname(),a,'->',q);done=True;break
   if done:break
  if not done:print('No safe stub',it['description'])
p.SaveBoard(str(path),b);print('Plane fanouts added',added)
