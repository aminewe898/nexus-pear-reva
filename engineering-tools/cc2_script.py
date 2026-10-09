from pathlib import Path
s=Path('work/finish_planes.py').read_text().split('items={')[0]
s+=r'''
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
  if math.hypot(max(l-q[0],0,q[0]-r),max(t-q[1],0,q[1]-d))<.31:return False
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
'''
Path('work/cc2_route.py').write_text(s)
