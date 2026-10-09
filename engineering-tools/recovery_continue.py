import subprocess
from pathlib import Path
cli=r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe';py=r'C:\Program Files\KiCad\10.0\bin\python.exe';general=r'C:\Python314\python.exe'
pro='outputs/nexus-pear-reva-reviewed/hardware/kicad/nexus-pear-reva/'
def run(*args):subprocess.run(args,check=True)
def script(n):run(py if n not in ['build_design_fixed'] else general,'work/recover_'+n+'.py')
def drc():run(cli,'pcb','drc','--format','json','--refill-zones','--save-board','--schematic-parity','--output','work/drc-new.json',pro+'nexus-pear-reva.kicad_pcb')
script('fix_new_clearance');drc();script('vbus_fix');script('raw_power_route');drc();script('ground_finish');drc();script('cc2_route');drc()
Path('work/reviewed-routed-backup.kicad_pcb').write_bytes(Path(pro+'nexus-pear-reva.kicad_pcb').read_bytes())
script('finish_new_layout');drc()
