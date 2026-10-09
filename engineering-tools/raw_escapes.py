from pathlib import Path
p=Path('work/raw_power_route.py');s=p.read_text().replace("for dx,dy in offsets:\n  q=", "if ref=='J1':offsets=[(0,-.62)]+offsets\n for dx,dy in offsets:\n  q=")
p.write_text(s)
