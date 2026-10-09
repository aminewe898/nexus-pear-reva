from pathlib import Path
import pcbnew as p,math,json
path=Path('outputs/nexus-pear-reva-reviewed/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path))
tracks=list(b.GetTracks());pads=[pa for f in b.GetFootprints() for pa in f.Pads()]
def mm(x):return p.ToMM(x)
def pt(a):return (mm(a.x),mm(a.y))
def distseg(q,a,c):
 dx=c[0]-a[0];dy=c[1]-a[1];n=dx*dx+dy*dy;t=0 if n==0 else max(0,min(1,((q[0]-a[0])*dx+(q[1]-a[1])*dy)/n));return math.hypot(q[0]-a[0]-t*dx,q[1]-a[1]-t*dy)
def safe(q,net):
 for t in tracks:
  if t.GetNetCode()==net:continue
  if isinstance(t,p.PCB_VIA):d=math.dist(q,pt(t.GetPosition()));r=mm(t.GetWidth(p.F_Cu))/2
  else:d=distseg(q,pt(t.GetStart()),pt(t.GetEnd()));r=mm(t.GetWidth())/2
  if d<.3+.2+r+.015:return False
 for pad in pads:
  if pad.GetNetCode()==net:continue
  box=pad.GetBoundingBox();lx=mm(box.GetLeft());rx=mm(box.GetRight());ty=mm(box.GetTop());by=mm(box.GetBottom())
  d=math.hypot(max(lx-q[0],0,q[0]-rx),max(ty-q[1],0,q[1]-by))
  if d<.515:return False
 return True
for t in tracks:
 if not isinstance(t,p.PCB_VIA) and t.GetWidth()<p.FromMM(.2):t.SetWidth(p.FromMM(.2))
added=[]
for t in tracks:
 if isinstance(t,p.PCB_VIA) or t.GetNetname() not in ['GND','+3V3']:continue
 a=pt(t.GetStart());c=pt(t.GetEnd());n=t.GetNetCode()
 for f in [.5,.25,.75,0,1]:
  q=(a[0]+f*(c[0]-a[0]),a[1]+f*(c[1]-a[1]))
  if any(math.dist(q,z)<1.2 for z in added):continue
  if safe(q,n):
   v=p.PCB_VIA(b);v.SetPosition(p.VECTOR2I(p.FromMM(q[0]),p.FromMM(q[1])));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(n);b.Add(v);tracks.append(v);added.append(q);break
p.SaveBoard(str(path),b);print('Added plane stitching vias:',len(added))
