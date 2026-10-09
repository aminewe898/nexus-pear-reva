from pathlib import Path
s=Path('work/finish_layout.py').read_text();s=s[:s.index('fps={')]
s+=r'''
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
'''
Path('work/finish_new_layout.py').write_text(s)
