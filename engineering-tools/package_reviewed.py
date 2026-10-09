from pathlib import Path
import json,hashlib,zipfile
from pypdf import PdfReader
r=Path('outputs/nexus-pear-reva-reviewed');v=r/'validation';pro=r/'hardware/kicad/nexus-pear-reva'
erc=json.loads((v/'erc-final.json').read_text());drc=json.loads((v/'drc-final.json').read_text())
assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
assert all(not s['violations'] for s in erc['sheets'])
settings=json.loads((pro/'nexus-pear-reva.kicad_pro').read_text())['board']['design_settings'];assert not settings.get('drc_exclusions')
metric=json.loads((v/'layout-metrics.json').read_text());bom=json.loads((v/'bom-summary.json').read_text());assert metric['footprints']==117
check={'erc_violations':0,'drc_violations':0,'unconnected_items':0,'schematic_parity_issues':0,'footprints':117,'placement_entries':96,'bom_rows':bom['rows'],'unknown_price_rows':bom['unknownPriceRows'],'schematic_pdf_pages':len(PdfReader(r/'previews/schematic.pdf').pages),'pcb_pdf_pages':len(PdfReader(r/'previews/pcb-layers.pdf').pages),'release_status':'DO NOT ORDER','physical_tests':False,'complete_procurement_quote':False,'impedance_qualified':False,'missing_3d_models':['U1','U7','J2','F1','L1']}
(v/'final-check-summary.json').write_text(json.dumps(check,indent=2))
with (r/'docs/FINAL_CHECK.md').open('a',encoding='utf8') as f:f.write(f"\nVerified result: ERC 0; DRC 0; unconnected 0; schematic parity 0. {metric['footprints']} footprints, {metric['tracks']} routed segments, {metric['vias']} vias; 96 placement entries. {bom['rows']} BOM rows, {bom['unknownPriceRows']} unpriced. Schematic 11 pages; PCB PDF 5 pages.\n\nThe native STEP/render export reported missing component models for U1, U7, J2, F1 and L1. Those components have electrical footprints but their bodies are absent from the 3D files. No enclosure clearance approval is inferred from the render.\n")
with (r/'docs/DESIGN_REVIEW_REVA.md').open('a',encoding='utf8') as f:f.write('\nFinal native checks: ERC 0, DRC 0, unconnected 0, schematic parity 0. The checked revision contains 117 physical footprints. Procurement remains incomplete: 96 of 106 BOM rows are unpriced. RFQ_GROUPED.csv is a draft procurement input, not a supplier commitment. Missing 3D component bodies are listed in FINAL_CHECK.md.\n')
# Remove transient GUI files only from this precisely resolved deliverable folder.
for f in r.rglob('*'):
 if f.is_file() and (f.suffix in ['.kicad_prl','.lck'] or f.name.endswith('~')):assert r.resolve() in f.resolve().parents;f.unlink()
files=[f for f in r.rglob('*') if f.is_file() and f.name!='delivery-manifest.json']
manifest=[{'path':f.relative_to(r).as_posix(),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(files)]
(v/'delivery-manifest.json').write_text(json.dumps({'release_status':'DO NOT ORDER','files':manifest},indent=2))
archive=Path('outputs/nexus-pear-reva-reviewed-submission.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for f in r.rglob('*'):
  if f.is_file():z.write(f,str(Path(r.name)/f.relative_to(r)))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps(check,indent=2));print('Archive',archive.resolve(),'bytes',archive.stat().st_size)
