import pcbnew as p,json
from pathlib import Path
path=Path('outputs/nexus-pear-reva/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path));items={t.m_Uuid.AsString():t for t in b.GetTracks()}
for uid in ['cb0ad747-e365-48ac-927f-2baea1fb922c','5670cb03-1823-4125-84cf-a0b6ad0c5c85','14485d18-4500-431b-b879-f2685f865dbc','45f33b8f-93e4-4bf5-a723-238a68a16295','19f58cb7-a8f9-446e-a20e-103acfc1150f','88795d20-790b-4cea-93f6-f38948dd765b','92cee17a-302c-4006-9e56-e6575db2d44f','d2d8634c-88d9-4d72-9aec-9e04accd9e89']:
 t=items[uid];print(uid,t.GetNetname(),list(p.ToMM(t.GetStart())),list(p.ToMM(t.GetEnd())))
