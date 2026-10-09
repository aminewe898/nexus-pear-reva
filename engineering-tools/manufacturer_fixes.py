from pathlib import Path
import pcbnew as p,json
out=Path('outputs/nexus-pear-reva');pro=out/'hardware/kicad/nexus-pear-reva';path=(pro/'nexus-pear-reva.kicad_pcb').resolve();b=p.LoadBoard(str(path));fps={f.GetReference():f for f in b.GetFootprints()}
d=json.load(open(out/'design_data.json'));codes={'47k':'47KL','887k':'887KL','34.8k':'34K8L','309k':'309KL','332k':'332KL'}
for a in d['parts']:
 if a['ref'].startswith('R') and a['value'] in codes:
  old=a['mpn'];a['mpn']='RC0805FR-07'+codes[a['value']]
  sh=pro/(a['sheet']+'.kicad_sch');sh.write_text(sh.read_text().replace('"'+old+'"','"'+a['mpn']+'"'))
  for field in fps[a['ref']].GetFields():
   if field.GetName()=='MPN':field.SetText(a['mpn'])
 if a['ref']=='J2':a['notes']=a['notes'].replace('SSH-003T-P0.2','SSHL-002T-P0.2')
 if a['ref']=='L1':a['notes']='Bourns C-series recommended pads 2.0x6.5mm, center spacing 4.5mm; local native snapshot corrected against manufacturer drawing.'
f=fps['L1'];x,y=p.ToMM(f.GetPosition())
for pad in f.Pads():
 pad.SetSize(p.VECTOR2I(p.FromMM(2),p.FromMM(6.5)));pad.SetPosition(p.VECTOR2I(p.FromMM(x+(-2.25 if pad.GetNumber()=='1' else 2.25)),p.FromMM(y)))
fp=pro/'Nexus.pretty/L_Bourns-SRN6028.kicad_mod';s=fp.read_text().replace('(at -2.35 0)','(at -2.25 0)').replace('(at 2.35 0)','(at 2.25 0)').replace('(size 1.6 5.7)','(size 2 6.5)');fp.write_text(s)
# Update honest geometric source notes in board and schematic.
for a in d['parts']:
 if a['ref'] in ('J2','L1'):
  for field in fps[a['ref']].GetFields():
   if field.GetName()=='Description':field.SetText(a['notes'])
for sh in pro.glob('*.kicad_sch'):sh.write_text(sh.read_text().replace('SSH-003T-P0.2','SSHL-002T-P0.2'))
json.dump(d,open(out/'design_data.json','w'),indent=2);p.SaveBoard(str(path),b)
r=json.load(open('work/drc-new.json'));print('Unconnected:')
for v in r['unconnected_items']:print(v['items'])
print('Violations:')
for v in r['violations']:
 if v['type'] not in ('silk_overlap','silk_over_copper'):print(v['type'],v['items'])
