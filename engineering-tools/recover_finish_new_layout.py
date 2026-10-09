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

# Keep routing vias out of assembly SMD pads; module thermal construction is audited separately.
def inpad(q):
 for pad in pads:
  if pad.GetAttribute()!=p.PAD_ATTRIB_SMD:continue
  box=pad.GetBoundingBox();margin=.05
  if p.ToMM(box.GetLeft())-margin<q[0]<p.ToMM(box.GetRight())+margin and p.ToMM(box.GetTop())-margin<q[1]<p.ToMM(box.GetBottom())+margin:return True
 return False
offsets=sorted([(i*.25,k*.25) for i in range(-12,13) for k in range(-12,13)],key=lambda z:math.hypot(*z))
moved=0;blocked=[]
for v in list(b.GetTracks()):
 if not isinstance(v,p.PCB_VIA):continue
 a=pt(v.GetPosition())
 if not inpad(a):continue
 net=v.GetNetCode();b.RemoveNative(v);done=False
 for dx,dy in offsets:
  q=(a[0]+dx,a[1]+dy)
  if inpad(q) or not clear(a,q,net,p.F_Cu):continue
  v.SetPosition(xy(q));b.Add(v)
  tr=p.PCB_TRACK(b);tr.SetStart(xy(a));tr.SetEnd(xy(q));tr.SetWidth(p.FromMM(.2));tr.SetLayer(p.F_Cu);tr.SetNetCode(net);b.Add(tr)
  # Existing via linked both outer layers; add back stub when needed.
  if any(not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.B_Cu and (math.dist(pt(t.GetStart()),a)<.001 or math.dist(pt(t.GetEnd()),a)<.001) for t in b.GetTracks()):
   tr=p.PCB_TRACK(b);tr.SetStart(xy(a));tr.SetEnd(xy(q));tr.SetWidth(p.FromMM(.2));tr.SetLayer(p.B_Cu);tr.SetNetCode(net);b.Add(tr)
  moved+=1;done=True;break
 if not done:b.Add(v);blocked.append(a)
print('Vias removed from SMD pads',moved,'blocked',blocked)

fps={f.GetReference():f for f in b.GetFootprints()}
# Place every visible annotation against actual copper and graphic extents.
for g in b.Drawings():
 if not isinstance(g,p.PCB_TEXT):continue
 old=g.GetText()
 if old=='NEXUS PEAR / REV A CANDIDATE':g.SetText('NEXUS PEAR / REV A: PEAR PRESSURE');g.SetPosition(xy((80,32)))
 elif old=='DO NOT ORDER - SEE DESIGN REVIEW':g.SetText('DO NOT ORDER - NO SMOKE SPEEDRUNS');g.SetPosition(xy((100,119)))
 elif old=='MIC / TOP':g.SetText('MIC / SAY LESS');g.SetPosition(xy((44,33)))
 elif old=='RF U.FL ON MODULE':g.SetPosition(xy((62,82)))
 elif old=='DISPLAY / VERIFY CABLE':g.SetText('DISPLAY / GH15 / 3V3');g.SetPosition(xy((110,46)))
 elif old=='STEREO AMP HARNESS':g.SetPosition(xy((44,56)))
 elif old=='USB-C 5V / DEVICE':g.SetText('USB-C / 5V 3A');g.SetPosition(xy((62,119)))
def rect(x):
 r=x.GetBoundingBox();return tuple(p.ToMM(v) for v in [r.GetLeft(),r.GetTop(),r.GetRight(),r.GetBottom()])
def overlap(a,c,m=.16):return not(a[2]+m<c[0] or c[2]+m<a[0] or a[3]+m<c[1] or c[3]+m<a[1])
texts=[];obs=list(pads)
for f in b.GetFootprints():
 obs += [g for g in f.GraphicalItems() if g.GetLayer()==p.F_SilkS]
 texts += [g for g in [f.Reference(),f.Value()] if g.GetLayer()==p.F_SilkS and g.IsVisible()]
texts += [g for g in b.Drawings() if isinstance(g,p.PCB_TEXT) and g.GetLayer()==p.F_SilkS]
offsets=sorted([(i*.5,j*.5) for i in range(-20,21) for j in range(-20,21)],key=lambda z:math.hypot(*z))
fail=[]
for text in texts:
 a=pt(text.GetPosition());text.SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));text.SetTextSize(xy((.8,.8)));text.SetTextThickness(p.FromMM(.12));done=False
 for dx,dy in offsets:
  q=(a[0]+dx,a[1]+dy);text.SetPosition(xy(q));r=rect(text)
  if r[0]<30.3 or r[1]<30.3 or r[2]>129.7 or r[3]>119.7:continue
  if any(overlap(r,rect(o)) for o in obs if o!=text):continue
  done=True;break
 if not done:fail.append(text.GetText())
 obs.append(text)
print('Annotation placement failures',fail)
p.SaveBoard(str(path),b)
