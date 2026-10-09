import pcbnew as p
from pathlib import Path
path=Path('outputs/nexus-pear-reva-reviewed/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path));fps={f.GetReference():f for f in b.GetFootprints()}
def xy(a):return p.VECTOR2I(p.FromMM(a[0]),p.FromMM(a[1]))
for t in list(b.GetTracks()):b.RemoveNative(t)
for ref,pos in {'R7':(48,104.1),'R8':(48,101.5),'C9':(66,43)}.items():fps[ref].SetPosition(xy(pos))
fps['C9'].SetOrientationDegrees(180)
def pad(r,n):return next(a for a in fps[r].Pads() if a.GetNumber()==str(n))
def pos(r,n):return tuple(p.ToMM(pad(r,n).GetPosition()))
def route(r,n,z,m,mid=[],w=.25):
 a=pad(r,n);pts=[pos(r,n)]+mid+[pos(z,m)]
 for x,y in zip(pts,pts[1:]):
  t=p.PCB_TRACK(b);t.SetStart(xy(x));t.SetEnd(xy(y));t.SetLayer(p.F_Cu);t.SetWidth(p.FromMM(w));t.SetNet(a.GetNet());b.Add(t)
route('U5',5,'L1',1,[(68.65,47),(69.65,48)],.6)
route('U5',6,'C9',1,[(67.1375,44.5)],.25)
route('C9',2,'U5',5,[(64.95,41.5),(68.65,41.5),(68.65,47)],.25)
route('C8',1,'U5',2,[],.6);route('U5',2,'U5',3,[],.35)
route('L1',2,'C10',1,[(76.525,48)],.8);route('L1',2,'C11',1,[(76.525,48)],.8)
# Kelvin feedback avoids switch copper; source the sense trace at output capacitor.
route('C10',1,'U5',1,[(76.525,40),(62.8,40),(62.8,44.5),(64.35,46.05)],.25)
route('R8',2,'U1',13,[(50.5,101.5),(51.83,102.83)],.2)
route('R7',2,'U1',14,[(50.5,104.1)],.2)
p.SaveBoard(str(path),b);p.ExportSpecctraDSN(b,str(Path('work/nexus.dsn').resolve()))
