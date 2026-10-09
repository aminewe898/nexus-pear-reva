from pathlib import Path
import pcbnew as p
path=Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path))
changes={'NEXUS PEAR / REV A CANDIDATE':'NEXUS PEAR / REV A: PEAR PRESSURE','DO NOT ORDER - SEE DESIGN REVIEW':'DO NOT ORDER - NO SMOKE SPEEDRUNS','MIC / TOP':'MIC / SAY LESS'}
for t in b.Drawings():
 if isinstance(t,p.PCB_TEXT) and t.GetText() in changes:t.SetText(changes[t.GetText()])
p.SaveBoard(str(path),b)
