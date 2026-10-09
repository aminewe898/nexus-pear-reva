from pathlib import Path
import json,pcbnew as p,math
path=Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path));j=json.load(open('outputs/nexus-pear-reva/validation/drc-stitched.json'))
for t in list(b.GetTracks()):
 if isinstance(t,p.PCB_VIA) and str(t.m_Uuid.AsString()) in ['043624a3-37d4-4b9d-aac9-035fb8413f47','0592523f-7f03-43c6-83b7-2e58d6102162']:b.RemoveNative(t)
for t in b.GetTracks():
 if t.GetNetname()=='CC2_ADC' and not isinstance(t,p.PCB_VIA):
  for method in ['Start','End']:
   v=getattr(t,'Get'+method)();x,y=p.ToMM(v)
   if 65.4<x<65.8 and 69.5<y<70.2:getattr(t,'Set'+method)(p.VECTOR2I(p.FromMM(x-.06),p.FromMM(y)))
fps={f.GetReference():f for f in b.GetFootprints()}
def xy(q):return p.VECTOR2I(p.FromMM(q[0]),p.FromMM(q[1]))
for ref,pos in {'R9':(44,81),'R27':(80,84.8)}.items():fps[ref].Reference().SetPosition(xy(pos))
for ref,pos in {'TP15':(44,78),'TP16':(39,98),'TP7':(95,44)}.items():fps[ref].Value().SetPosition(xy(pos))
p.SaveBoard(str(path),b)
