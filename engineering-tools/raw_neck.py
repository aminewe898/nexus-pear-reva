from pathlib import Path
p=Path('work/raw_power_route.py');s=p.read_text();s=s.replace('def ok(q):','def ok(q,a,z):');s=s.replace("if any(math.dist(q,v)<.91 for v in viaobs):return False","limit=.81 if min(math.dist(q,a),math.dist(q,z))<.4 else .91\n if any(math.dist(q,v)<limit for v in viaobs):return False")
s=s.replace('if not ok(pos):continue','if not ok(pos,a,z):continue');s=s.replace("tr.SetWidth(p.FromMM(.8));tr.SetLayer(p.In2_Cu)","tr.SetWidth(p.FromMM(.6 if min(math.dist(x,a),math.dist(y,a),math.dist(x,z),math.dist(y,z))<.4 else .8));tr.SetLayer(p.In2_Cu)")
p.write_text(s)
