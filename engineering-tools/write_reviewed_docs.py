from pathlib import Path
import json
r=Path('outputs/nexus-pear-reva-reviewed');d=r/'docs';data=json.loads((r/'design_data.json').read_text());parts=data['parts'];bom=json.loads((r/'validation/bom-summary.json').read_text())
def put(name,body):(d/name).write_text(body.strip()+'\n',encoding='utf8')
put('ARCHITECTURE.md','''# The pear has range — architecture

NEXUS PEAR is a USB-powered desktop interface to a remote AI service. ESP32-S3-WROOM-1U-N16R8 provides Wi-Fi, Bluetooth, native USB, 16 MB flash and 8 MB PSRAM. The enclosure concept is a pear; the display is a normal rectangle. No battery, charger, local language-model inference or USB host is included.

USB-C VBUS passes a 3 A/24 V PTC, TVS and TPS25940L protected switch. An always-on LDO supplies TUSB320LAI and hardware logic. Only a source advertising 3 A on CC enables the main supply. AP63203 generates shared 3.3 V for the processor, display, microphone and microSD. The two audio modules use protected 5 V; TXU0104 translates and isolates their I2S signals. GPIO38 enables audio data, with a hardware pull-down.

The Waveshare 29318 module provides ST7796S SPI IPS graphics and FT6336U two-point capacitive touch. A digital I2S microphone mounts at the top acoustic opening. Two MAX98357A modules drive separate 8-ohm Visaton speakers at the lower sides. Six physical lower-right keys share an ADC ladder. A real external Taoglas RP-SMA antenna connects to the module U.FL socket through CAB.774.

Carrier: 100 x 90 mm, four layers. F.Cu and B.Cu carry most signals; In1.Cu is ground, In2.Cu is 3.3 V with isolated raw-power/CC routing. Full functionality still needs firmware, harness assembly, enclosure and bench qualification. DO NOT ORDER is the release status.
''')
put('PROCESSOR_DECISION.md','''# Picking the brain — no hype tax

| Platform | Relevant fit | Decision |
|---|---|---|
| ESP32-S3 + PSRAM | Wi-Fi/BLE, native USB, I2S and SPI; external-antenna module available | Selected for remote inference and modest partial-screen UI |
| ESP32-P4 + radio companion | More graphics throughput; extra processor/radio and power complexity | Better if full-screen animation becomes essential |
| STM32H743 + radio | Strong real-time/audio resources; separate network hardware | More integration cost for this network-first interface |
| RP2350 + radio | Flexible PIO; separate Wi-Fi and additional UI integration | No clear advantage for this feature set |
| Small Linux SBC | Rich application stack and graphics | More boot, storage, power and enclosure overhead |

This decision depends on the SPI display's roughly 4.88 ideal full frames/s at 12 MHz. It supports low-motion interfaces and partial updates. A requirement for continuous 30/60 full frames/s requires a different display bus or platform. No current complete assembled-system quotes were obtained for the alternatives.
''')
put('DISPLAY_RESEARCH.md','''# Screen time, but make it engineering

Selected: Waveshare 3.5inch Capacitive Touch LCD, SKU 29318. Public schematic, pin table and controller datasheets replace the previous account-gated NXP candidate. ST7796S, native 320 x 480 RGB565, rotated to 480 x 320 landscape, IPS, FT6336U two-point touch. Module outline 61 x 92.44 mm; active area 48.96 x 73.44 mm. Manufacturer price observed: USD 18.99, 2026-10-07; shipping and taxes excluded.

Use 3.3 V mode: J2 pins 1 and 2 connect to the carrier's same 3.3 V rail. Do not apply 5 V. Carrier header SM15B-GHS-TB(LF)(SN) mates to GHR-15V-S with SSHL-002T-P0.2 contacts (26-30 AWG, 0.76-1.0 mm insulation). SSH-003T-P0.2 is not the specified compatible contact. Confirm the numbered connector orientation on both ends before powering; a cable is not assumed straight-through by color.

ST7796S write cycle minimum 66 ns gives a 15.15 MHz ceiling. Set SPI writes to 12 MHz (83.3 ns) and reads at most 6 MHz (150 ns minimum read cycle). Start bring-up at 1-5 MHz. One RGB565 full frame is 307200 bytes; ideal transmission takes 204.8 ms at 12 MHz, or 4.88 frames/s before protocol overhead. For 30 Hz UI scheduling, use small partial updates, typically 10-15% of the screen. No 30 Hz full-screen claim is made. Budget display current at 200 mA despite the maker FAQ's approximately 63 mA operating example.

NXP LCD-PAR-S035 was rejected because detailed panel/mating information was not publicly obtainable. BuyDisplay ER-TFT035IPS-6-4405 remained unqualified after datasheet access failure. Their pin assignments are not used in this revision.

Mechanical concept: landscape display spans board coordinates x=33.78..126.22, y=17..78 in a separate front plane. It overhangs the carrier's top by 13 mm, leaving room above the lower-right keys. The enclosure must accommodate that extension, display depth, microphone opening and antenna connector. This is an allocation drawing, not a completed enclosure or a verified clearance stack.
''')
put('AUDIO_DESIGN.md','''# Let the pear cook — audio and microphone

Two Adafruit 3006 MAX98357A mono modules create stereo outputs. BCLK/WS/data are shared after TXU0104 translates 3.3 V logic to protected 5 V. The translator has power-off isolation/Ioff; its OE defaults low through 100 kOhm. Output damping resistors are 33 ohm; amplifier data inputs have 100 kOhm pull-downs. GPIO38 enables audio only after supply checks.

Breakout channel selection includes its internal 1 MOhm pull-up and IC 100 kOhm pull-down: SD to 5 V through 82 kOhm selects left (approximately 2.85 V), 560 kOhm selects right (approximately 1.09 V). GAIN floats for nominal 9 dB. Verify these levels on the purchased module revision. Speakers: Visaton K28.40, MPN 2945, 8 ohm, 2 W rated. Class-D bridge terminals must never connect to ground or a grounded oscilloscope clip.

The simultaneous-load design allowance caps acoustic output at 0.75 W per channel. Unrestricted full scale can exceed the power budget. Firmware must implement a calibrated limit; that implementation and calibration are not delivered or tested here.

Adafruit 3421 SPH0645LM4H uses 3.3 V and separate 33-ohm-damped 3.3 V microphone BCLK/WS. It does not receive 5 V translator outputs. Target shared I2S clock: 48 kHz x 64 bits = 3.072 MHz. Capture the appropriate signed slot and resample to 16 kHz for upload if required. Begin with half-duplex push-to-talk. Echo cancellation, voice quality and acoustic isolation remain implementation/bench work. Place the bottom-port microphone at a top enclosure acoustic opening with a sealed path; do not block its port.
''')
put('POWER_BUDGET.md','''# Watt could go wrong? — power budget

Required source: standard non-PD USB-C 5 V supply advertising 3 A on CC. TUSB320LAI in fixed sink/GPIO mode performs source-current detection. OUT1/OUT2 are high/high when unattached, high/low for default current, low/high for 1.5 A, low/low for 3 A. Dual NOR logic and 2N7002 clamp eFuse enable unless both outputs are low. Internal dead-battery Rd is used; external Rd and MCU CC voltage inference were removed. Main hardware deliberately stays off on ordinary 500 mA/1.5 A ports. Native USB debug needs a 3 A-capable data port/hub; alternatively use a 3.3 V UART adapter and a separate qualified power supply. UART reference must not power the board.

TPS25940LRVCR supplies reverse blocking, UVLO, OVP, current limiting and latched fault behavior. ILIM=34.8 kOhm gives nominal 2.558 A, estimated 2.330..2.791 A including datasheet +/-8% and resistor 1%. UVLO uses 309 kOhm/100 kOhm (approximately 4.05 V nominal); OVP uses 475 kOhm/100 kOhm, 0.1% (5.693 V nominal, approximately 5.568..5.817 V). 47 nF dV/dt capacitor targets approximately 19.5 ms at 5 V. Power-good threshold uses 332 kOhm/100 kOhm. Read exact thresholds and hysteresis in the TI datasheet; these estimates are not bench measurements.

F1 is Littelfuse 1812L300/24SLER: 3 A hold at 23 C, 24 V rated, 6 A trip, 30 mOhm maximum post-trip resistance. Manufacturer derating gives 2.45 A at 40 C, 1.85 A at 60 C. Full concurrent load is not qualified above 40 C. The previous Bourns 3 A/16 V order code was invalid and is removed. SMBJ10A pulse clamp is 17 V at its specified test current, below eFuse 20 V absolute maximum and AON LDO 30 V maximum. TVS pulse energy and fault tolerances still need qualification. CC protection is ground-referenced bidirectional PESD5V0S2BT; it does not provide a 20 V CC short-to-VBUS guarantee. Non-PD 5 V operation is the supported mode.

| 3.3 V load | Conservative allowance |
|---|---:|
| ESP32-S3 Wi-Fi/transient budget | 900 mA |
| Display/backlight/touch | 200 mA |
| microSD transient | 200 mA |
| Microphone | 20 mA |
| Miscellaneous | 50 mA |
| Total | 1370 mA / 4.521 W |

At 80% buck efficiency and protected input 4.0 V this needs 1.413 A. Two 0.75 W audio channels at 80% efficiency need 0.469 A; add 40 mA amplifier/buffer allowance and 1 mA AON. Total approximately 1.923 A; with 20% contingency, 2.307 A, or 11.54 W at 5 V. This leaves only about 23 mA beyond the contingency before the estimated minimum eFuse limit. Treat the cap as mandatory and measure simultaneous Wi-Fi, SD, backlight and stereo peaks. Reduce audio/brightness if any rail droops or input protection trips.

AP63203 is a 2 A buck. Corrected SRN6028C-3R9M is 3.3 A RMS, 3.9 A saturation, 28 mOhm. Output MLCC capacitance under DC bias is still a measured/manufacturer-curve release gate. Raw bus capacitance is less than 1 uF by nominal populated values; the main 10 uF input reservoir sits after controlled inrush. Bench startup, unplug/replug, short, reverse-path leakage, thermal and minimum-source-voltage tests remain mandatory. Numbers above are design allowances, not measured performance.
''')
pin=['# Pin lore — the actual wiring','','These tables are generated from the checked native design. Nets are engineering identifiers; NC pins are omitted. Shared peripheral 3.3 V removes independently powered display/microphone/SD domains. Do not externally power any harness.','']
for ref in ['U1','J1','J2','J3','J4','J5','J6','J7','J8']:
 p=next(x for x in parts if x['ref']==ref);pin+=['## '+ref+' — '+p['value'],'','| Pin | Signal | Net |','|---|---|---|']+[f"| {a['num']} | {a['name']} | {a['net']} |" for a in p['pins'] if a['net']]+['']
pin+=['Boot/reset retain ESP32 defaults. IO35/36/37 are reserved by octal PSRAM and unused. IO3/45/46 straps are unused. GPIO38 only enables translated audio signals. GPIO1 reads a one-key-at-a-time ADC ladder; calibration and released-key saturation handling are firmware requirements.',''];put('PIN_ASSIGNMENTS.md','\n'.join(pin))
put('FOOTPRINT_AUDIT.md','''# Trust issues, measured in millimeters — footprint audit

Native DRC includes library matching and schematic parity; validation/footprint-pad-inventory.json records every physical pad, drill, size and net. All assigned symbol pins match the installed footprint pads. This proves native consistency, not that every manufacturer's tolerance drawing has been approved.

| Item | Drawing/pin check and corrective action | Remaining qualification |
|---|---|---|
| ESP32-S3-WROOM-1U | Exact module pin map; octal PSRAM exclusions; native module land/ground construction | Antenna certification, reflow and thermal-pad process |
| GCT USB4105-GF-A | Manufacturer pad numbering including native SH grounded; duplicated USB signals mapped | Mechanical sample fit; exact shell/tail tolerance overlay |
| TPS25940L RVC | 20 pins + EP; complete IN/OUT banks; 3 x 4 mm WQFN, 0.5 mm pitch | Assembly EP paste and thermal qualification |
| TUSB320LAI RWB | 12-pin 1.6 x 1.6 mm X2QFN, 0.4 mm pitch; fixed sink mapping | Fine-pitch assembly process |
| TLV76033 DBZ | Corrected pin 1 OUT, 2 IN, 3 GND | Physical first-article orientation |
| SN74LVC2G02 DCT | DCT 0.65 mm-pitch SSOP-8 chosen to meet existing clearance | First-article pin 1 inspection |
| TXU0104 PW | 14-pin TSSOP, split supplies and correct direction/pin mapping | Ioff and OE test in actual assembly |
| SRN6028C-3R9M | Corrected local lands to 2.0 x 6.5 mm, centers +/-2.25 mm; native previous pattern was wrong | Solderability, height and thermal measurement |
| Littelfuse 1812L300/24SLER | Corrected lands to 1.78 x 3.45 mm, centers +/-2.465 mm; manufacturer gap 3.15 mm | Actual height/3D accuracy and thermal derating |
| JST SM15B-GHS-TB | GH 1.25 mm pitch; corrected exact mating contact SSHL-002T-P0.2 | Full tolerance overlay and cable sample |
| Omron B3F1000 | 6 x 6 mm switch; 6.5 x 4.5 mm pad spacing; 1.1 mm holes; horizontal duplicate-pin pairs match manufacturer drawing | Switch-height/enclosure stack |
| Samtec TSW | Exact 4/6/7-position MPNs and pin maps | Manufacturer drill tolerance and exact assembled harness drawing |
| 0805/1206 passives, SOT-23, SOT-23-6, LED, TVS | Local library consistency and populated pad/net inventory | Per-MPN maximum-body/polarity overlay and MLCC DC-bias curves remain open |

R21 zero-ohm order code is corrected to RC0805JR-070RL. E96 order codes and OVP 0.1% parts are recorded in the BOM. The 3D view contains generic component models and omits off-board display/audio/antenna mechanics; it cannot approve enclosure clearances. No footprint exceptions or relaxed design rules were used to obtain a pass.
''')
put('TEST_PLAN_REVA.md','''# The vibe check needs a multimeter — bring-up plan

No bench tests have been performed. This is the required acceptance plan for a first article.

1. Inspect exact MPNs, connector orientation, shorts, EP soldering and corrected inductor/PTC lands. Check unpowered rail resistance before connecting modules.
2. Use current-limited power. Confirm AON starts and main stays off with no CC attachment, default-current attachment and 1.5 A advertisement. Attach a 3 A-advertising source in both cable orientations; record startup/inrush and unplug/replug behavior. No MCU intervention may defeat hardware gating.
3. Verify UVLO/OVP, eFuse fault latch/reset, load-short response and thermal behavior with a controlled supply/load. Do not apply an unsupported 20 V fault to a populated board. Measure raw TVS and protected-rail pulse overshoot with suitable equipment.
4. Measure 3.3 V output ripple, minimum-voltage margin and 3.3 V rail startup under 1.37 A load. Confirm actual biased MLCC capacitance meets regulator requirements. Measure input PTC, eFuse, inductor, copper and connector temperatures at worst simultaneous load and 40 C ambient.
5. Exercise each power-off ordering case with external modules attached. Check translator Ioff and MCU pin voltage/current with its rail off. Externally powered peripheral harnesses are not supported.
6. Verify USB enumeration, firmware recovery and transfer error rates with representative qualified 3 A data ports/cables. Fabricator must confirm stackup and 90-ohm differential requirements; inspect via discontinuities and skew before release. Use 3.3 V UART recovery when the data host cannot advertise 3 A.
7. Bring up display at 1-5 MHz, then 12 MHz writes and <=6 MHz reads. Confirm reset/touch interrupt sequencing, colors, landscape orientation and partial-update latency. Measure full-brightness current.
8. Verify all six ADC keys individually, bounce and held-key handling. Multi-key rollover is not provided. Check SD writes during Wi-Fi traffic and display refresh.
9. Check stereo selection voltages, channel mapping, microphone slot/clock format and signed sample scaling. Calibrate firmware to <=0.75 W/channel during concurrent load. Measure peak input current, speaker distortion and acoustic feedback. Keep bridge outputs isolated from ground.
10. Fit display, microphone, speakers, six keys, cable strain relief and real antenna into an enclosure. Review the 13 mm display overhang allocation. Test RF performance, EMI/ESD and applicable antenna approvals.

Record instruments, supply/cable/firmware revision, waveforms, limits and results. A clean ERC/DRC is a prerequisite; it does not replace any of these measurements.
''')
sources=['# Receipts, because "trust me bro" is not a datasheet','','Research date: 2026-10-07. Official documentation is the basis of the redesign. Indexed supplier prices are explicitly weaker than current cart evidence. No supplier order or RFQ was sent.','','| References | Manufacturer | Exact MPN | Official source |','|---|---|---|---|']
seen={}
for p in parts:
 if p.get('mpn') and p.get('datasheet') and p.get('footprint') and not p['ref'].startswith(('TP','H')):
  k=(p['manufacturer'],p['mpn'],p['datasheet']);seen.setdefault(k,[]).append(p['ref'])
for (m,mpn,url),refs in seen.items():sources.append(f"| {' '.join(refs)} | {m} | {mpn} | [Source]({url}) |")
sources+=['','Display: [product](https://www.waveshare.com/product/3.5inch-capacitive-touch-lcd.htm), [wiki](https://www.waveshare.com/wiki/3.5inch_Capacitive_Touch_LCD), [public schematic](https://files.waveshare.com/wiki/3.5inch%20Capacitive%20Touch%20LCD/3.5inch_Capacitive_Touch_LCD_Schematic.pdf), [ST7796S](https://files.waveshare.com/wiki/common/ST7796S_Datasheet.pdf), [FT6336U](https://files.waveshare.com/wiki/common/FT6336U_Datasheet.pdf), [JST GH drawing](https://www.jst-mfg.com/product/pdf/eng/eGH.pdf).','', 'Protection references: [TPS25940](https://www.ti.com/lit/ds/symlink/tps25940.pdf), [TUSB320LAI](https://www.ti.com/lit/ds/symlink/tusb320lai.pdf), [TLV760](https://www.ti.com/lit/ds/symlink/tlv760.pdf), [TXU0104](https://www.ti.com/lit/ds/symlink/txu0104.pdf), [Littelfuse Low Rho drawing/derating](https://www.littelfuse.com/assetdocs/low-rho-datasheet-update?assetguid=b786faf0-de16-4763-9d22-6b8080943caf).','', 'Software: [KiCad 10 CLI](https://docs.kicad.org/10.0/en/cli/cli.html). KiCad 10.0.1 supplied native ERC/DRC and manufacturing exports. Local autorouting was followed by manual buck/USB/power corrections and native checks. Routing provenance is retained as engineering evidence.','', f"BOM: {bom['rows']} rows, {bom['unknownPriceRows']} rows without prices. Observed USD subtotal {bom['quotedSubtotals']['USD']:.3f} across ten rows is not a total procurement quote. Indexed prices, currency, import, VAT, shipping, PCB assembly, enclosure and storage-card cost are not a committed purchase price."]
put('SOURCES.md','\n'.join(sources))
put('DESIGN_REVIEW_REVA.md','''# The pear is on trial — final design review

**DO NOT ORDER. Engineering review submission, not a fabrication release.** No hardware or firmware was tested.

| Previous gate | Work completed in this revision | What remains |
|---|---|---|
| Display documentation/mate/timing | Replaced NXP with public Waveshare 29318; released SPI/pin map, exact GH mate/contact and conservative timing/current budget | Cable sample, reset/touch bring-up and enclosure fit |
| USB protection/source-current/input margin | Hardware 3 A CC gating, AON controller, 5.2 A-rated eFuse, UV/OV/reverse protection and slew; corrected 24 V PTC | Fault/inrush/thermal measurements; voltage and current-limit tolerance validation |
| Powered-off back-power | Removed separate display/SD/mic rails; fail-safe TXU0104 for 5 V audio and default-low OE | First-article Ioff and all power-order measurements |
| Footprints and procurement | Corrected inductor/PTC lands, LDO pins, GH contacts and invalid order codes; complete native pad/net inventory and grouped RFQ | Full manufacturer tolerance overlays, MLCC DC-bias curves, exact cable drawing and complete live quotes |
| Critical routing | MCU moved near USB, short manual USB/buck paths, dedicated ground plane, routed power and repaired vias/clearances | Fabricator stackup/90-ohm pair approval, signal-integrity, copper-drop and thermal validation |

This revision closes the identified circuit defects in the native files and produces a reviewable candidate. It does not claim all release gates are closed. USB routing is shorter but is not qualified controlled impedance. Generic 3D models cannot certify mechanics. Full-scale audio is not supported concurrently by the budget: <=0.75 W/channel must be calibrated in firmware. Above 40 C ambient, PTC derating can constrain the load further.

Check the final native reports and pad inventory in validation/. No ERC/DRC exclusions or clearance reductions were introduced. All exported files are regenerated from the revised project in the reviewed directory; the older open-session save is excluded.

Top decisions: S3 external-antenna module; public SPI display; hardware 3 A input qualification; shared 3.3 V plus isolated audio; 4-layer carrier with manual critical routes. Top risks: tight current budget, unqualified USB impedance, MLCC bias/thermal margin, incomplete mechanical/polarity tolerance audits and incomplete live procurement quotes.
''')
put('FINAL_CHECK.md','''# Final checks — the receipts

See validation/erc-final.json and drc-final.json for native results, footprint-pad-inventory.json for pads/nets and layout-metrics.json for actual routing counts/lengths. The BOM and placement export are checked against native footprint values, MPNs and coordinates. Manufacturing exports and PDFs are regenerated from this revision.

The schematic power sheet is enlarged to A2 to contain the added protection circuit. Rendered PDF pages, PCB layers and board render are visually inspected. Final delivery-manifest.json records file sizes and SHA256 hashes.

Release remains DO NOT ORDER for the explicit bench, procurement, mechanics and impedance items in DESIGN_REVIEW_REVA.md. Neither a tested prototype nor completed firmware is claimed. Product purpose, legitimate sources and engineering limitations are retained.
''')
(r/'README.md').write_text('''# NEXUS PEAR REV A — pear pressure

**DO NOT ORDER — engineering review submission.** Revised project: 2026-10-07.

ESP32-S3-WROOM-1U-N16R8, 16 MB flash/8 MB PSRAM, Waveshare 29318 IPS touch display (320 x 480 native / 480 x 320 landscape), two-point FT6336U, digital I2S microphone, stereo MAX98357A modules, 8-ohm speakers, optional microSD, real U.FL-to-RP-SMA external antenna, six ADC keys and bottom USB-C. Carrier 100 x 90 mm, four layers, no battery. Design peak allowance 11.54 W including 20% contingency and an enforced 0.75 W/channel audio cap; no measured peak is claimed.

Open hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pro in KiCad 10. Native schematic, PCB, local symbols and local footprints are included. previews/schematic.pdf is the complete eleven-sheet schematic; previews/pcb-layers.pdf and board-3d.png support review. Manufacturing Gerbers, Excellon drill files, placement CSV, BOM and STEP are under hardware/manufacturing/. Do not submit those as an approved fabrication order.

hardware/BOM_REVA.csv contains exact candidate MPNs; hardware/RFQ_GROUPED.csv groups quantities for procurement. Pricing is incomplete. SUBMISSION.md is the short cover note; docs/ contains the architecture, processor comparison, display/audio/power calculations, pin map, footprint review, sources and first-article test plan. docs/DESIGN_REVIEW_REVA.md identifies every remaining release gate. Native ERC/DRC reports, pad inventory, route metrics and hashed delivery manifest are under validation/.

The revised circuit adds hardware Type-C current qualification and protected input power, removes independently powered 3.3 V peripherals, isolates audio signals and replaces the undocumented display. Corrected manufacturer footprints and routing are in this project's native files. Firmware, physical qualification, complete procurement and enclosure design remain to be completed.
''',encoding='utf8')
(r/'SUBMISSION.md').write_text('''# NEXUS PEAR REV A — pear pressure

A small desktop device with a normal rectangular touch screen, stereo speakers, a top microphone, Wi-Fi, a real external antenna and six buttons. The pear has range. The antenna is doing an actual job.

This submission includes an editable eleven-sheet KiCad design, a routed four-layer 100 x 90 mm carrier, BOM/RFQ, manufacturing exports, PDFs, a board render and engineering calculations. Remote services perform model inference; the ESP32-S3 handles interface, networking and audio.

The revision replaces the display with a publicly documented module, adds hardware 3 A USB source qualification and protected power, addresses power-off signal injection, corrects manufacturer land patterns/order codes, and improves critical routing. Final ERC and DRC results are included with the actual native files.

**Engineering review candidate — DO NOT ORDER.** Physical startup/fault/thermal/audio/USB tests, fabricator impedance approval, complete live quotes and remaining mechanical/footprint tolerance checks are still required. Firmware and a tested prototype are not part of this submission. Read docs/DESIGN_REVIEW_REVA.md for the precise completion status. The connectivity vibe check passed; release needs measurements.
''',encoding='utf8')
print('Rebuilt all review documents from revised data.')
