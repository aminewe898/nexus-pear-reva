import pcbnew as p,json,math
from pathlib import Path
path=Path('outputs/nexus-pear-reva-reviewed/hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path));r=json.load(open('work/drc-new.json'));items={t.m_Uuid.AsString():t for t in b.GetTracks()}

lookup={'cb0ad747-e365-48ac-927f-2baea1fb922c':('I2S_BCLK_SRC',(66.532,68.6742)), '5670cb03-1823-4125-84cf-a0b6ad0c5c85':('POWER_GOOD',(42.3873,99.1132)), '14485d18-4500-431b-b879-f2685f865dbc':('POWER_GOOD',(42.4889,96.9141)), '45f33b8f-93e4-4bf5-a723-238a68a16295':('POWER_GOOD',(42.3873,97.0157)), '19f58cb7-a8f9-446e-a20e-103acfc1150f':('CC1',(54.0432,111.5994)), '88795d20-790b-4cea-93f6-f38948dd765b':('CC1',(54.1998,111.756)), '92cee17a-302c-4006-9e56-e6575db2d44f':('CC1',(54.275,111.8)), 'd2d8634c-88d9-4d72-9aec-9e04accd9e89':('CC1',(54.231,111.756))}
for key,(net,pos) in lookup.items():
 matches=[t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetNetname()==net and math.dist(tuple(p.ToMM(t.GetStart())),pos)<.0001]
 lengths={'cb0ad747-e365-48ac-927f-2baea1fb922c':4.2944,'5670cb03-1823-4125-84cf-a0b6ad0c5c85':2.0975,'14485d18-4500-431b-b879-f2685f865dbc':.8660,'45f33b8f-93e4-4bf5-a723-238a68a16295':.1437,'19f58cb7-a8f9-446e-a20e-103acfc1150f':.2435,'88795d20-790b-4cea-93f6-f38948dd765b':.2215,'92cee17a-302c-4006-9e56-e6575db2d44f':.0622,'d2d8634c-88d9-4d72-9aec-9e04accd9e89':.0312}
 matches=sorted(matches,key=lambda t:abs(p.ToMM(t.GetLength())-lengths[key]))
 if not matches:raise RuntimeError(key)
 items[key]=matches[0]
def xy(a):return p.VECTOR2I(p.FromMM(a[0]),p.FromMM(a[1]))
def tr(a,z,net,w=.2,layer=p.F_Cu):
 t=p.PCB_TRACK(b);t.SetStart(xy(a));t.SetEnd(xy(z));t.SetWidth(p.FromMM(w));t.SetLayer(layer);t.SetNetCode(net);b.Add(t)
remove=set()
for v in r['violations']:
 if v['type'] in ('via_dangling','copper_edge_clearance'):
  remove.update(i['uuid'] for i in v['items'] if i['uuid'] in items and isinstance(items[i['uuid']],p.PCB_VIA))
for u in remove:b.RemoveNative(items[u])
ends=[(66.532,68.6742),(63.4954,65.6376)]
pg=[(42.3873,99.1132),(42.3873,97.0157),(42.4889,96.9141),(42.4889,96.0481)]
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):continue
 for getter,setter in [(t.GetStart,t.SetStart),(t.GetEnd,t.SetEnd)]:
  q=tuple(p.ToMM(getter()))
  if t.GetNetname()=='I2S_BCLK_SRC' and any(math.dist(q,a)<.0001 for a in ends):setter(xy((q[0]+.06,q[1]-.06)))
  if t.GetNetname()=='POWER_GOOD' and any(math.dist(q,a)<.0001 for a in pg):setter(xy((q[0]+.1,q[1])))
cc=['19f58cb7-a8f9-446e-a20e-103acfc1150f','88795d20-790b-4cea-93f6-f38948dd765b','92cee17a-302c-4006-9e56-e6575db2d44f','d2d8634c-88d9-4d72-9aec-9e04accd9e89'];net=items[cc[0]].GetNetCode()
for u in cc:b.RemoveNative(items[u])
tr((54.275,111.8),(53.7997,111.8),net);tr((53.7997,111.8),(53.7997,111.5994),net)
fps={f.GetReference():f for f in b.GetFootprints()};vbus=next(a for a in fps['J1'].Pads() if a.GetNumber()=='A4').GetNetCode()
def via(q,net):
 v=p.PCB_VIA(b);v.SetPosition(xy(q));v.SetWidth(p.FromMM(.6));v.SetDrill(p.FromMM(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(net);b.Add(v)
for a,z in [((45.6,113.72),(45.6,112.6)),((50.4,113.72),(50.4,112.6))]:tr(a,z,vbus,.4);via(z,vbus)
tr((36.8625,110),(34.8,110),vbus,.8);via((34.8,110),vbus)
tr((34.8,110),(37.4,112.6),vbus,.8,p.In2_Cu);tr((37.4,112.6),(45.6,112.6),vbus,.8,p.In2_Cu);tr((45.6,112.6),(50.4,112.6),vbus,.8,p.In2_Cu)
p.SaveBoard(str(path),b)
