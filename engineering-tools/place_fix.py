from pathlib import Path
s=Path('work/build_design_fixed.py').read_text().replace("[(i,'OUT','+5V','power_out') for i in range(4,9)]","[(i,'OUT','+5V','power_out' if i==4 else 'passive') for i in range(4,9)]")
s=s.replace('SN74LVC2G02DCUR','SN74LVC2G02DCTR').replace('Package_SO:VSSOP-8_2.3x2mm_P0.5mm','Package_SO:SSOP-8_2.95x2.8mm_P0.65mm')
s=s.replace('# Reposition critical loops',"# Reposition critical loops")
s=s.replace("# Procurement-only assumptions", "# Procurement-only assumptions")
s=s.replace("# Schematic source", "extra={'TP1':(33,112),'TP2':(33,83),'TP4':(49,81),'TP7':(108,48),'TP3':(51,84),'U9':(60,115),'C23':(65,115),'U2':(48,110),'U3':(55,116.5),'C6':(33,105),'D2':(38,105),'F1':(39,112),'C21':(38,92),'C25':(70,62),'R50':(63,56),'R49':(59.5,56),'R48':(56,56),'C1':(78,91),'D1':(73,74),'SW7':(84,114),'C9':(68.3,43.6)}\nfor d in parts:\n if d['ref'] in extra:d['xy']=extra[d['ref']]\n# Schematic source")
Path('work/build_design_fixed.py').write_text(s)
