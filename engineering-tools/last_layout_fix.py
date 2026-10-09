import pcbnew as p,re
from pathlib import Path
pro=Path('outputs/nexus-pear-reva-reviewed/hardware/kicad/nexus-pear-reva');path=(pro/'nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path));f=next(f for f in b.GetFootprints() if f.GetReference()=='L1')
for g in list(f.GraphicalItems()):
 if g.GetLayer()==p.F_SilkS:f.Remove(g)
lib=pro/'Nexus.pretty/L_Bourns-SRN6028.kicad_mod';s=lib.read_text();s=re.sub(r'\t\(fp_line.*?\n\t\)\n',lambda m:'' if 'F.SilkS' in m[0] else m[0],s,flags=re.S);lib.write_text(s)
def xy(a):return p.VECTOR2I(p.FromMM(a[0]),p.FromMM(a[1]))
v=next(t for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetname()=='VBUS' and abs(p.ToMM(t.GetPosition().x)-31.75)<.001)
t=p.PCB_TRACK(b);t.SetStart(xy((33,109)));t.SetEnd(v.GetPosition());t.SetLayer(p.In2_Cu);t.SetWidth(p.FromMM(.2));t.SetNetCode(v.GetNetCode());b.Add(t)
p.SaveBoard(str(path),b)
