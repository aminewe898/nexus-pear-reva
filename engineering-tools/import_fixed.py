from pathlib import Path
import pcbnew as p
path=Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path));print('Import',p.ImportSpecctraSES(b,str(Path('work/nexus-fixed.ses').resolve())));p.SaveBoard(str(path),b)
