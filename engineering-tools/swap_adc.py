from pathlib import Path
p=Path('work/build_design.py');s=p.read_text();s=s.replace("'IO5':'LCD_D1'","'IO5':'CC2_ADC'").replace("'IO14':'CC2_ADC'","'IO14':'LCD_D1'");p.write_text(s)
