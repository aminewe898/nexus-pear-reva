from pathlib import Path
s=Path('work/finish_planes.py').read_text();s=s[:s.index('items={')]
s += r'''
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
'''
Path('work/raw_fanout.py').write_text(s)
