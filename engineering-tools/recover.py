from pathlib import Path
import zipfile
for p in Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva-backups').glob('*.zip'):
 with zipfile.ZipFile(p) as z:
  for n in z.namelist():
   if n.endswith('.kicad_pcb'):
    s=z.read(n);print(p.name,n,len(s),b'TXU0104' in s)
    if b'TXU0104' in s:Path('work/recovered-new.kicad_pcb').write_bytes(s)
