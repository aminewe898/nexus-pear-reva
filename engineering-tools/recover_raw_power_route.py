import pcbnew as p,json,math
from pathlib import Path
path=Path('outputs/nexus-pear-reva-reviewed/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path))
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

# Replace raw-input escapes with geometry-checked vias. Route power on In2, preserving In1 ground.
for t in list(b.GetTracks()):
 if t.GetNetname()=='VBUS' or (t.GetNetname()=='CC2' and not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and 49.7<=p.ToMM(t.GetStart().x)<=54.1 and 112.2<=p.ToMM(t.GetStart().y)<=113.75):b.RemoveNative(t)
fps={f.GetReference():f for f in b.GetFootprints()};raw=[]
for ref,num in [('J1','A4'),('J1','A9'),('F1','1'),('TP1','1')]:
 item=next(a for a in fps[ref].Pads() if a.GetNumber()==num);a=pt(item.GetPosition());net=item.GetNetCode();done=False
 offsets=sorted([(i*.25,j*.25) for i in range(-16,17) for j in range(-16,17)],key=lambda z:math.hypot(*z))
 if ref=='J1':offsets=[(0,-.62)]+offsets
 for dx,dy in offsets:
  q=(a[0]+dx,a[1]+dy)
  if not clear(a,q,net,p.F_Cu):continue
  v=p.PCB_VIA(b);v.SetPosition(xy(q));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(net);b.Add(v)
  t=p.PCB_TRACK(b);t.SetStart(xy(a));t.SetEnd(xy(q));t.SetLayer(p.F_Cu);t.SetWidth(p.FromMM(.2));t.SetNetCode(net);b.Add(t);raw.append(q);done=True;print(ref,num,a,q);break
 if not done:print('BLOCKED',ref,num)

from heapq import heappush,heappop
viaobs=[pt(t.GetPosition()) for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetname()!='VBUS']
rectobs=[]
for a in pads:
 if a.GetAttribute()==p.PAD_ATTRIB_SMD or a.GetNetCode()==net:continue
 z=a.GetBoundingBox();rectobs.append(tuple(p.ToMM(v) for v in [z.GetLeft(),z.GetTop(),z.GetRight(),z.GetBottom()]))
def ok(q,a,z):
 if not 31<q[0]<60 or not 103<q[1]<119:return False
 limit=.81 if min(math.dist(q,a),math.dist(q,z))<.4 else .91
 if any(math.dist(q,v)<limit for v in viaobs):return False
 for l,t,r,d in rectobs:
  if math.hypot(max(l-q[0],0,q[0]-r),max(t-q[1],0,q[1]-d))<.61:return False
 return True
def route(a,z):
 start=tuple(round(v*10) for v in a);end=tuple(round(v*10) for v in z);queue=[(0,start)];cost={start:0};prev={}
 while queue:
  _,q=heappop(queue)
  if q==end:break
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
   n=(q[0]+dx,q[1]+dy);pos=(n[0]/10,n[1]/10)
   if not ok(pos,a,z):continue
   v=cost[q]+math.hypot(dx,dy)
   if v>=cost.get(n,1e9):continue
   cost[n]=v;prev[n]=q;heappush(queue,(v+math.dist(n,end),n))
 if end not in cost:raise RuntimeError(('No raw input path',a,z))
 pts=[end]
 while pts[-1]!=start:pts.append(prev[pts[-1]])
 pts=[a]+[(q[0]/10,q[1]/10) for q in reversed(pts)]+[z]
 for x,y in zip(pts,pts[1:]):
  if math.dist(x,y)<.0001:continue
  tr=p.PCB_TRACK(b);tr.SetStart(xy(x));tr.SetEnd(xy(y));tr.SetWidth(p.FromMM(.6 if min(math.dist(x,a),math.dist(y,a),math.dist(x,z),math.dist(y,z))<.4 else .8));tr.SetLayer(p.In2_Cu);tr.SetNetCode(net);b.Add(tr)
 print('Raw power path',a,z,len(pts))
for q in raw[1:]:route(raw[0],q)
p.SaveBoard(str(path),b)
