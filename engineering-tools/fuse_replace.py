from pathlib import Path
import json,re,pcbnew as p
out=Path('outputs/nexus-pear-reva-reviewed');pro=out/'hardware/kicad/nexus-pear-reva';data=json.load(open(out/'design_data.json'));d=next(d for d in data['parts'] if d['ref']=='F1');old=d.copy();d.update(value='3A / 24V PTC',mpn='1812L300/24SLER',manufacturer='Littelfuse',datasheet='https://www.littelfuse.com/assetdocs/low-rho-datasheet-update?assetguid=b786faf0-de16-4763-9d22-6b8080943caf',notes='Manufacturer Low Rho table: 3A hold, 24V, R1max30mOhm; recommended pads 1.78x3.45mm, 3.15mm inner gap. Derates to 2.45A at40C and1.85A at60C.',unit_cost=2.63,currency='USD',supplier='DigiKey',supplier_sku='18-1812L300/24SLERCT-ND',availability='DigiKey page 7549 in stock; checked 2026-10-07',quote_url='https://www.digikey.com/en/products/detail/littelfuse-inc/1812L300-24SLER/12807021')
for sh in [pro/'00_power.kicad_sch',pro/'Nexus.kicad_sym']:
 s=sh.read_text()
 for k in ['value','mpn','datasheet','notes']:s=s.replace(json.dumps(old[k]),json.dumps(d[k]))
 sh.write_text(s)
b=p.LoadBoard(str((pro/'nexus-pear-reva.kicad_pcb').resolve()));f=next(f for f in b.GetFootprints() if f.GetReference()=='F1');f.SetValue(d['value'])
for field in f.GetFields():
 if field.GetName() in ['MPN','Datasheet','Description']:field.SetText(d[{'MPN':'mpn','Datasheet':'datasheet','Description':'notes'}[field.GetName()]])
x,y=p.ToMM(f.GetPosition())
for a in f.Pads():a.SetSize(p.VECTOR2I(p.FromMM(1.78),p.FromMM(3.45)));a.SetPosition(p.VECTOR2I(p.FromMM(x+(-2.465 if a.GetNumber()=='1' else 2.465)),p.FromMM(y)))
for g in f.GraphicalItems():
 if g.GetLayer()==p.F_CrtYd:
  for getter,setter in [(g.GetStart,g.SetStart),(g.GetEnd,g.SetEnd)]:
   a,z=p.ToMM(getter());setter(p.VECTOR2I(p.FromMM(x+(3.6 if a>x else -3.6)),p.FromMM(y+(2.0 if z>y else -2.0))))
p.SaveBoard(str((pro/'nexus-pear-reva.kicad_pcb').resolve()),b)
lib=pro/'Nexus.pretty/Fuse_1812_4532Metric.kicad_mod';s=lib.read_text().replace('(at -2.1375 0)','(at -2.465 0)').replace('(at 2.1375 0)','(at 2.465 0)').replace('(size 1.125 3.4)','(size 1.78 3.45)')
# Match courtyard edge changes by serializing only this footprint from the corrected board.
f=next(f for f in b.GetFootprints() if f.GetReference()=='F1');print('Save corrected F1 footprint',p.FootprintSave(str((pro/'Nexus.pretty').resolve()),f))
json.dump(data,open(out/'design_data.json','w'),indent=2)
