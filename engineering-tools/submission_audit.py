from pathlib import Path
import pcbnew as p,json,csv,collections
root=Path('outputs/nexus-pear-reva-reviewed');b=p.LoadBoard(str((root/'hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb').resolve()));fps={f.GetReference():f for f in b.GetFootprints()};inventory=[]
for ref,f in fps.items():
 inventory.append({'ref':ref,'footprint':str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName()),'pads':[{'number':a.GetNumber(),'net':a.GetNetname() or None,'at_mm':list(p.ToMM(a.GetPosition())),'size_mm':list(p.ToMM(a.GetSize())),'drill_mm':list(p.ToMM(a.GetDrillSize()))} for a in f.Pads()]})
json.dump(inventory,open(root/'validation/footprint-pad-inventory.json','w'),indent=2)
data=json.load(open(root/'design_data.json'));checks=[]
for d in data['parts']:
 if not d['footprint']:continue
 f=fps[d['ref']];assert f.GetValue()==d['value'],d['ref'];d['xy']=list(p.ToMM(f.GetPosition()));d['angle']=f.GetOrientationDegrees()
 for pin in d['pins']:
  matching=[a for a in f.Pads() if a.GetNumber()==pin['num']];assert matching,(d['ref'],pin['num'])
  if pin['net']:assert all(a.GetNetname()==pin['net'] for a in matching),(d['ref'],pin['num'],pin['net'])
json.dump(data,open(root/'design_data.json','w'),indent=2)
with open(root/'hardware/BOM_REVA.csv',newline='',encoding='utf8') as f:bom=list(csv.DictReader(f))
for r in bom:
 ref=r['Reference']
 if ref not in fps:continue
 assert r['Value']==fps[ref].GetValue(),ref
 mp=next((x for x in fps[ref].GetFields() if x.GetName()=='MPN'),None);assert mp is not None and mp.GetText()==r['MPN'],(ref,r['MPN'])
assert (root/'hardware/BOM_REVA.csv').read_bytes()==(root/'hardware/manufacturing/bom/BOM_REVA.csv').read_bytes()
with open(root/'hardware/manufacturing/position/nexus-pear-reva.csv',newline='',encoding='utf8') as f:pos=list(csv.DictReader(f))
for row in pos:
 f=fps[row['Ref']];x,y=p.ToMM(f.GetPosition());assert abs(float(row['PosX'])-x)<.00001 and abs(float(row['PosY'])+y)<.00001
print('Verified',len(fps),'footprints, all assigned pin nets, BOM values/MPNs and',len(pos),'position entries. Refreshed stale pad inventory and canonical placements.')


