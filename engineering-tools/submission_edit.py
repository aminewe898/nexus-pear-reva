from pathlib import Path
root=Path('outputs/nexus-pear-reva')
heads={
'ARCHITECTURE.md':'# The pear has range — architecture',
'PROCESSOR_DECISION.md':'# Picking the brain — no hype tax',
'DISPLAY_RESEARCH.md':'# Screen time, but make it engineering',
'AUDIO_DESIGN.md':'# Let the pear cook — audio and microphone',
'POWER_BUDGET.md':'# Watt could go wrong? — power budget',
'PIN_ASSIGNMENTS.md':'# Pin lore — the actual wiring',
'FOOTPRINT_AUDIT.md':'# Trust issues, measured in millimeters — footprint audit',
'TEST_PLAN_REVA.md':'# The vibe check needs a multimeter — bring-up plan',
'SOURCES.md':'# Receipts, because "trust me bro" is not a datasheet',
'DESIGN_REVIEW_REVA.md':'# The pear is on trial — final design review'}
for name,title in heads.items():
 p=root/'docs'/name;s=p.read_text(encoding='utf8');s=title+'\n'+s.split('\n',1)[1]
 s=s.replace('## Software/tool documentation fetched through Context7','## Software and tool documentation')
 s=s.replace("the user's definition of done",'the release checklist').replace('## Defects fixed before final checks','## Bugs evicted before the final checks').replace('## Five mandatory release gates','## Five things still blocking the fab button')
 p.write_text(s,encoding='utf8')
p=root/'README.md';s=p.read_text(encoding='utf8').replace('# NEXUS PEAR REV A — DO NOT ORDER','# NEXUS PEAR REV A — pear pressure').replace('## Open and review','## The receipts').replace('## What must change before order','## Before the fab button gets main-character energy');s=s.replace('An actual editable KiCad 10.0.1 engineering candidate:', '**DO NOT ORDER — engineering review submission.**\n\nTiny desk pear, big network energy. An editable KiCad 10.0.1 engineering candidate:');p.write_text(s,encoding='utf8')
(root/'SUBMISSION.md').write_text('''# NEXUS PEAR REV A — pear pressure

A little desk device with a screen, stereo speakers, a microphone, Wi-Fi and six physical buttons. The enclosure concept is a pear; the display is a normal rectangle. We have standards. And corners.

The ESP32-S3 handles the interface, audio and networking. Remote servers handle the heavy model work. Two I2S amplifier modules drive real 8-ohm speakers, and a digital microphone handles speech capture. The visible antenna actually connects to the radio — decorative RF cosplay was not invited.

## What exists

- Editable KiCad schematic with 11 sheets, a routed four-layer 100 × 90 mm carrier, and local symbols/footprints.
- BOM, Gerbers, drills, placement data, schematic/PCB PDFs and a board render.
- Architecture comparisons, bandwidth and power calculations, pin tables, source links, footprint audit and bring-up plan.
- Final native checks: ERC zero violations; DRC zero violations, zero unconnected items and zero schematic/PCB mismatches.

## The honest part

**DO NOT ORDER.** This is a design-review submission, not a tested device or fabrication-ready release. The display's detailed specifications and cable still need verification. USB power protection/current handling and input-switch margin need changes. Powered-off peripheral signals need isolation or proven safe sequencing. Footprint/mechanical audits, sourcing and critical layout review remain open. No hardware, firmware, thermal, acoustic or EMI result is being claimed.

The power estimate is about 8 W at peak, or 10–10.3 W with contingency. The BOM has only five priced rows; separate quoted subtotals are EUR 6.705 and USD 47.85, with 79 rows unpriced. That is not the total build cost.

The pear passed the connectivity vibe check. The release checklist still wants receipts. See docs/DESIGN_REVIEW_REVA.md for the exact blockers and README.md for every file.
''',encoding='utf8')
# Wording only: preserve reference designators, nets, values, pin numbers and release status.
pro=root/'hardware/kicad/nexus-pear-reva'
for p in pro.glob('*.kicad_sch'):
 s=p.read_text(encoding='utf8').replace('DO NOT ORDER - candidate circuit; unresolved release gates in design review','DO NOT ORDER - no smoke speedruns. Read the design review.')
 p.write_text(s,encoding='utf8')
print('Edited public prose and schematic annotations; sources, limits and engineering identifiers retained.')
