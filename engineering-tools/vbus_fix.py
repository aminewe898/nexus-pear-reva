from pathlib import Path
import pcbnew as p,math
path=Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path))
def xy(a):return p.VECTOR2I(p.FromMM(a[0]),p.FromMM(a[1]))
def tr(a,z,net,w=.2,layer=p.F_Cu):
 t=p.PCB_TRACK(b);t.SetStart(xy(a));t.SetEnd(xy(z));t.SetWidth(p.FromMM(w));t.SetLayer(layer);t.SetNetCode(net);b.Add(t)
for t in list(b.GetTracks()):
 if t.GetNetname()=='VBUS':b.RemoveNative(t)
pg=[(42.4873,99.1132),(42.4873,97.0157),(42.5889,96.9141),(42.5889,96.0481)]
old=(41.9122,96.6752)
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):
  if t.GetNetname()=='EFUSE_EN' and math.dist(tuple(p.ToMM(t.GetPosition())),old)<.0001:t.SetPosition(xy((old[0]-.12,old[1])))
  continue
 for getter,setter in [(t.GetStart,t.SetStart),(t.GetEnd,t.SetEnd)]:
  q=tuple(p.ToMM(getter()))
  if t.GetNetname()=='POWER_GOOD' and any(math.dist(q,a)<.0001 for a in pg):setter(xy((q[0]-.1,q[1])))
  if t.GetNetname()=='EFUSE_EN' and math.dist(q,old)<.0001:setter(xy((q[0]-.12,q[1])))
fps={f.GetReference():f for f in b.GetFootprints()};net=next(a for a in fps['J1'].Pads() if a.GetNumber()=='A4').GetNetCode()
def via(q):
 v=p.PCB_VIA(b);v.SetPosition(xy(q));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(net);b.Add(v)
for pts in [[(45.6,113.72),(46,114.12),(46,116.3)],[(50.4,113.72),(50,114.12),(50,116.3)],[(36.8625,110),(35,110.5)],[(33,109),(35,110.5)]]:
 for a,z in zip(pts,pts[1:]):tr(a,z,net,.4 if pts[0][0]>40 else .8)
for q in [(46,116.3),(50,116.3),(35,110.5)]:via(q)
for a,z in zip([(35,110.5),(38,113.5),(38,116.3),(46,116.3),(50,116.3)],[(38,113.5),(38,116.3),(46,116.3),(50,116.3)]):tr(a,z,net,.8,p.In2_Cu)
p.SaveBoard(str(path),b)
sh=path.parent/'00_power.kicad_sch';sh.write_text(sh.read_text().replace('C series selected, not obsolete SRN6028. Native footprint is old series; comparison pending.','Bourns C-series recommended pads 2.0x6.5mm, center spacing 4.5mm; local native snapshot corrected against manufacturer drawing.'))
