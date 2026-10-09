from pathlib import Path
import subprocess,json,shutil
r=Path('outputs/nexus-pear-reva-reviewed').resolve();pro=r/'hardware/kicad/nexus-pear-reva';cli='C:/Program Files/KiCad/10.0/bin/kicad-cli.exe';pcb=pro/'nexus-pear-reva.kicad_pcb';sch=pro/'nexus-pear-reva.kicad_sch'
# Larger power sheet keeps the additional protection circuit inside its page.
for f in pro.glob('*.kicad_sch'):
 if f.name=='00_power.kicad_sch':f.write_text(f.read_text(encoding='utf8').replace('(paper "A3")','(paper "A2")'),encoding='utf8')
history=Path('work/pre-final-export-history');history.mkdir(exist_ok=True)
for f in (r/'validation').glob('*'):
 if f.is_file() and f.name!='bom-summary.json':shutil.copy2(f,history/f.name);f.unlink()
def run(*args):
 p=subprocess.run([cli,*map(str,args)],capture_output=True,text=True);print(p.stdout.strip(),p.stderr.strip(),flush=True);assert p.returncode==0,args
run('sch','erc','--format','json','--output',r/'validation/erc-final.json',sch)
run('pcb','drc','--format','json','--schematic-parity','--refill-zones','--save-board','--output',r/'validation/drc-final.json',pcb)
run('sch','export','pdf','--output',r/'previews/schematic.pdf',sch)
run('pcb','export','pdf','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Silkscreen','--common-layers','Edge.Cuts','--mode-multipage','--output',r/'previews/pcb-layers.pdf',pcb)
run('pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts','--output',str(r/'hardware/manufacturing/gerbers')+'/',pcb)
run('pcb','export','drill','--format','excellon','--output',str(r/'hardware/manufacturing/drill')+'/',pcb)
run('pcb','export','pos','--format','csv','--units','mm','--output',r/'hardware/manufacturing/position/nexus-pear-reva.csv',pcb)
run('pcb','render','--width','1600','--height','1200','--output',r/'previews/board-3d.png',pcb)
run('pcb','export','step','--output',r/'hardware/manufacturing/nexus-pear-reva.step',pcb)
