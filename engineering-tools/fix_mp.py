from pathlib import Path
s=Path('work/build_design_fixed.py').read_text();s=s.replace("# Reposition critical loops", "next(d for d in parts if d['ref']=='J2')['pins'].append(dict(num='MP',name='MOUNT',net='GND',type='passive'))\n# Reposition critical loops")
Path('work/build_design_fixed.py').write_text(s)
