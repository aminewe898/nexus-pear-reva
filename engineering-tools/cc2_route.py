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
  if (via or t.GetLayer()==layer) and sd(a,q,x,y)<.1+.2+r-.0001:return False
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
   if min(sd(a,q,corners[i],corners[(i+1)%4]) for i in range(4))<.2999:return False
 return True

from heapq import heappush,heappop
fps={f.GetReference():f for f in b.GetFootprints()};a=next(a for a in fps['U7'].Pads() if a.GetNumber()=='2');net=a.GetNetCode();start=pt(a.GetPosition());offsets=sorted([(i*.25,j*.25) for i in range(-12,13) for j in range(-12,13)],key=lambda z:math.hypot(*z))
for dx,dy in offsets:
 q=(start[0]+dx,start[1]+dy)
 if clear(start,q,net,p.F_Cu):break
else:raise RuntimeError('No CC2 safe escape')
v=p.PCB_VIA(b);v.SetPosition(xy(q));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(net);b.Add(v)
t=p.PCB_TRACK(b);t.SetStart(xy(start));t.SetEnd(xy(q));t.SetWidth(p.FromMM(.2));t.SetLayer(p.F_Cu);t.SetNetCode(net);b.Add(t)
a=q;z=(49.693,114.8009)
viaobs=[pt(t.GetPosition()) for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetCode()!=net]
lines=[(pt(t.GetStart()),pt(t.GetEnd()),p.ToMM(t.GetWidth())/2) for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.In2_Cu and t.GetNetCode()!=net]
rectobs=[]
for pad in pads:
 if pad.GetAttribute()==p.PAD_ATTRIB_SMD or pad.GetNetCode()==net:continue
 r=pad.GetBoundingBox();rectobs.append(tuple(p.ToMM(v) for v in [r.GetLeft(),r.GetTop(),r.GetRight(),r.GetBottom()]))
def ok(q):
 if not 45<q[0]<65 or not 107<q[1]<118:return False
 if any(math.dist(q,v)<.61 for v in viaobs):return False
 if any(ds(q,x,y)<r+.31 for x,y,r in lines):return False
 for l,t,r,d in rectobs:
  if math.hypot(max(l-q[0],0,q[0]-r),max(t-q[1],0,q[1]-d))<.2999:return False
 return True
begin=tuple(round(v*10) for v in a);end=tuple(round(v*10) for v in z);queue=[(0,begin)];cost={begin:0};prev={}
while queue:
 _,q=heappop(queue)
 if q==end:break
 for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
  n=(q[0]+dx,q[1]+dy)
  if not ok((n[0]/10,n[1]/10)):continue
  v=cost[q]+math.hypot(dx,dy)
  if v>=cost.get(n,1e9):continue
  cost[n]=v;prev[n]=q;heappush(queue,(v+math.dist(n,end),n))
if end not in cost:raise RuntimeError(('CC2 no path',a,z))
pts=[end]
while pts[-1]!=begin:pts.append(prev[pts[-1]])
pts=[a]+[(q[0]/10,q[1]/10) for q in reversed(pts)]+[z]
for x,y in zip(pts,pts[1:]):
 if math.dist(x,y)<.0001:continue
 t=p.PCB_TRACK(b);t.SetStart(xy(x));t.SetEnd(xy(y));t.SetWidth(p.FromMM(.2));t.SetLayer(p.In2_Cu);t.SetNetCode(net);b.Add(t)
p.SaveBoard(str(path),b);print('CC2 escape',a,'path nodes',len(pts))
