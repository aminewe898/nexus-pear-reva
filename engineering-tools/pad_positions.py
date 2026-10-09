import pcbnew as p
from pathlib import Path
b=p.LoadBoard(str(Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve()));fs={f.GetReference():f for f in b.GetFootprints()}
fs['J7'].SetPosition(p.VECTOR2I(p.FromMM(75.5),p.FromMM(98)))
for r in ['U1','U5','C8','C9','L1','C10','C11','R7','R8','U2','J1']:
 print(r,[(a.GetNumber(),a.GetNetname(),list(p.ToMM(a.GetPosition()))) for a in fs[r].Pads() if r!='U1' or 'USB' in a.GetNetname()])
p.SaveBoard('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb',b)
