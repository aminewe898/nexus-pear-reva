from pathlib import Path
p=Path('work/cc2_route.py');s=p.read_text().replace("sd(a,q,x,y)<.1+.2+r+.01","sd(a,q,x,y)<.1+.2+r-.0001");p.write_text(s)
