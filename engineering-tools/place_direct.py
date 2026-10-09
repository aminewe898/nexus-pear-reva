import pcbnew as p
from pathlib import Path
b=p.LoadBoard(str(Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve()));fps={f.GetReference():f for f in b.GetFootprints()}
for ref,xy in {'C6':(32.4,104),'SW7':(80,110),'J7':(77,98),'TP3':(51,84.7),'TP4':(44,72),'R33':(62,107.5)}.items():fps[ref].SetPosition(p.VECTOR2I(p.FromMM(xy[0]),p.FromMM(xy[1])))
p.SaveBoard('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb',b)
p.ExportSpecctraDSN(b,str(Path('work/nexus.dsn').resolve()))
