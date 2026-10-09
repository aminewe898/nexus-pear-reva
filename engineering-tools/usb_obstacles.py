import pcbnew as p,math
from pathlib import Path
b=p.LoadBoard(str(Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve()))
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA) and math.dist(tuple(p.ToMM(t.GetPosition())),(50.4,113.72))<3:print('via',t.GetNetname(),list(p.ToMM(t.GetPosition())))
 elif not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and min(math.dist(tuple(p.ToMM(t.GetStart())),(50.4,113.72)),math.dist(tuple(p.ToMM(t.GetEnd())),(50.4,113.72)))<2:print(t.GetNetname(),list(p.ToMM(t.GetStart())),list(p.ToMM(t.GetEnd())))
