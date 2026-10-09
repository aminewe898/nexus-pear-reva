from pathlib import Path
s=Path('work/last_layout_fix.py').read_text();i=s.index('def xy');s='import pcbnew as p\nfrom pathlib import Path\npro=Path("outputs/nexus-pear-reva-reviewed/hardware/kicad/nexus-pear-reva");path=(pro/"nexus-pear-reva.kicad_pcb").resolve();b=p.LoadBoard(str(path))\n'+s[i:];Path('work/tp_internal_fix.py').write_text(s)
