from pathlib import Path
p=Path('work/cc2_route.py');s=p.read_text().replace("<.31:return False","<.2999:return False");p.write_text(s)
