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

# Replace raw-input escapes with geometry-checked vias. Route power on In2, preserving In1 ground.
for t in list(b.GetTracks()):
 if t.GetNetname()=='VBUS':b.RemoveNative(t)
fps={f.GetReference():f for f in b.GetFootprints()};raw=[]
for ref,num in [('J1','A4'),('J1','A9'),('F1','1'),('TP1','1')]:
 item=next(a for a in fps[ref].Pads() if a.GetNumber()==num);a=pt(item.GetPosition());net=item.GetNetCode();done=False
 offsets=sorted([(i*.25,j*.25) for i in range(-16,17) for j in range(-16,17)],key=lambda z:math.hypot(*z))
 for dx,dy in offsets:
  q=(a[0]+dx,a[1]+dy)
  if not clear(a,q,net,p.F_Cu):continue
  v=p.PCB_VIA(b);v.SetPosition(xy(q));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(net);b.Add(v)
  t=p.PCB_TRACK(b);t.SetStart(xy(a));t.SetEnd(xy(q));t.SetLayer(p.F_Cu);t.SetWidth(p.FromMM(.2));t.SetNetCode(net);b.Add(t);raw.append(q);done=True;print(ref,num,a,q);break
 if not done:print('BLOCKED',ref,num)
p.SaveBoard(str(path),b)
