from pathlib import Path
import json
out=Path('outputs/nexus-pear-reva');docs=out/'docs'
def write(name,s):(docs/name).write_text(s.strip()+'\n',encoding='utf8')
write('SOURCES.md','''# Sources and research provenance

Research date:2026-10-07. Official documents and reputable supplier listings were consulted. A search-index stock count is weaker evidence than a live cart result; access failures are explicitly retained. Price snippets are not procurement quotes. Detailed panel data could not be obtained despite available product/app-note pages. Document revisions below refer to the copies served during research.

| Item | Manufacturer / official datasheet / reference | Supplier / availability evidence |
|---|---|---|
| ESP32-S3-WROOM-1U-N16R8 |[Official module datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf),v1.8,2026-03-02; pin table/module land pattern |[DigiKey Spain](https://www.digikey.es/en/products/detail/espressif-systems/ESP32-S3-WROOM-1U-N16R8/16162641):EUR5.94 excluding VAT,0 stock. [Mouser Spain](https://www.mouser.es/es/ProductDetail/Espressif-Systems/ESP32-S3-WROOM-1U-N16R8?qs=Li%252BoUPsLEns6V0Pr5KRJtw%3D%3D):indexed6887/EUR5.93; opening timed out, not live confirmed.|
| NXP LCD-PAR-S035 |[Official product/direct shop](https://www.nxp.com/design/design-center/development-boards-and-designs/LCD-PAR-S035);[AN14776](https://www.nxp.com/docs/en/application-note/AN14776.pdf),Rev1,2025-09-22;[UM12018 official community attachment](https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/MCX/4254/1/UM12018%20(3).pdf),Rev2,2024-08-23,Table21 |NXP direct USD29/>100 units shown; detailed schematic/panel datasheet account-gated. AN14776 web reader worked though direct shell fetch returned403. Public host manual signal map does not prove panel mating geometry.|
| Waveshare alternative |[Product29318](https://www.waveshare.com/3.5inch-capacitive-touch-lcd.htm);[Wiki/manual](https://www.waveshare.com/wiki/3.5inch_Capacitive_Touch_LCD) |Official shop USD18.99/in-stock at research. Controller/panel timings still require application qualification.|
| BuyDisplay alternative |[ER-TFT035IPS-6-4405 datasheet endpoint](https://www.buydisplay.com/download/manual/ER-TFT035IPS-6-4405_Datasheet.pdf) |HTTP403; exact touch option/price/stock not verified.|
| ESP32-P4 |[Official function-board reference](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html),v1.5.2 |Architecture comparison only; no carrier/component quote obtained.|
| STM32H743 |[Official STM32H743XI product/datasheet links](https://www.st.com/en/microcontrollers-microprocessors/stm32h743xi.html) |Comparison only, package procurement not selected.|
| RP2350 |[Official product/datasheet links](https://www.raspberrypi.com/products/rp2350/) |Comparison only.|
| Raspberry Pi Zero2W |[Official product/documentation](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) |Comparison only; OS/mechanical overhead judged, no current assembled-system quote.|
| AP63203WU-7 |[Official Diodes datasheet](https://www.diodes.com/assets/Datasheets/AP63200-AP63201-AP63203-AP63205.pdf),Rev3-2,2024-11; typical fixed3.3 V circuit |[Mouser Spain](https://www.mouser.es/en/ProductDetail/Diodes-Incorporated/AP63203WU-7?qs=u16ybLDytRZ1JqxbuLkMJw%3D%3D),EUR0.765 indexed/stock0; other European Mouser listing reported~17010. Regional/index discrepancies require live quote; not classified globally unavailable.|
| TPS22918DBVR |[TI product](https://www.ti.com/product/TPS22918);[datasheet](https://www.ti.com/lit/ds/symlink/tps22918.pdf),SLVSD76C,2017-07;CT equation and2 A rating |DigiKey Spain indexed5994601 showed0; DBVT alternate packaging may be available, but substitution/procurement not released.|
| USBLC6-2SC6 |[ST official datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf),DS4260Rev7; USB/CC ESD topology |DigiKey1040559 indexed Spain0; third-party counts not adopted; live price/stock unqualified.|
| GCTUSB4105-GF-A |[GCT product](https://gct.co/connector/usb4105);[official drawing](https://gct.co/files/drawings/usb4105.pdf) including recommended footprint |Supplier quote not obtained. Drawing downloaded successfully; full pad overlay still pending.|
| BournsSRN6028C-3R9M |[Official current-series datasheet](https://www.bourns.com/data/global/pdfs/SRN6028C.pdf);[series page](https://www.bourns.com/products/magnetic-products/details/power-inductors-smd-semi-shielded/srn6028c) |[DigiKey exact C-series listing](https://www.digikey.com/en/products/detail/bourns-inc/SRN6028C-3R9M/18785115); price/live stock not captured.|
| BournsMF-MSMF300/16X-2 |[Official MF-MSMF datasheet](https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf) |Exact distributor quote, physical drawing and thermal derating need final review.|
| Adafruit3006/MAX98357A |[Adafruit product/direct supplier](https://www.adafruit.com/product/3006);[breakout pinout](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/pinouts);[Analog Devices chip datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf) |USD5.95 each, Add to Cart shown. Carrier uses2 modules. EU import/VAT/shipping excluded.|
| Adafruit3421/SPH0645LM4H |[Adafruit product/direct supplier](https://www.adafruit.com/product/3421);[pinout and clock guide](https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/pinouts);[datasheet/schematic downloads](https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/downloads) |USD6.95,Add to Cart shown. Full Knowles drawing/acoustic specifications not completely reviewed.|
| Adafruit4682microSD |[Official product/direct supplier](https://www.adafruit.com/product/4682);[3V-only breakout pinout](https://learn.adafruit.com/adafruit-microsd-spi-sdio/pinouts) |Page found; price/stock not captured. Exact revision/harness and card transient behavior pending.|
| Visaton2945K28.40/8Ohm |[Official driver specifications](https://www.visaton.de/en/products/drivers/miniature-speakers/k-2840-8-ohm) |[Mouser](https://www.mouser.com/en/ProductDetail/Visaton/2945?qs=bT6MOr62zwIiK6vhwf0QbA%3D%3D) indexed898;[TME Spain](https://www.tme.eu/es/details/vs-k28.40-8/altavoces/visaton/2945/) indexed200. Prices/live counts unqualified.|
| TaoglasGW.11.A153 |[Official datasheet](https://www.taoglas.com/datasheets/GW.11.A153.pdf),RevH,2026-08-31,up to3 dBi,84.4 x7.8 mm |[Mouser exact MPN](https://www.mouser.com/en/ProductDetail/Taoglas/GW.11.A153?qs=WUa1z%2FNV9%252B2Zy21V1WVQAg%3D%3D),indexed1963;price/live stock unverified. Older2.3 dBi specification must not be used.|
| TaoglasCAB.774 |[Official cable datasheet](https://www.taoglas.com/datasheets/CAB.774.pdf),U.FL toRP-SMA(F)100 mm drawing |Supplier quote absent. Text contains inconsistent generic connector/length wording; mechanical drawing and actual sample must settle gender/length.|
| SamtecTSW headers |[Official series/configurator/drawing](https://www.samtec.com/products/tsw),exact MPNs inBOM |Exact configuration and distributor quote pending.|
| OmronB3F1000 |[Official series/datasheet links](https://components.omron.com/us-en/products/switches/B3F) |Exact orderable variant/drawing and stock not completely audited.|
| MurataMLCC |[Official MLCC product search](https://www.murata.com/en-global/products/capacitor/mlcc),exact MPNs inBOM |DC-bias curves,land patterns and exact quotes not captured.|
| YageoRC0805 resistors |[Official product search](https://www.yageo.com/en/ProductSearch),exact candidateMPNs inBOM |Specific values/zero-ohm jumper designation and supplier quotes need qualification.|

## Software/tool documentation fetched through Context7

- [KiCad10 CLI](https://docs.kicad.org/10.0/en/cli/cli.html):ERC,DRC and native exports. Installed version10.0.1.
- [ESP-IDF5.5.4 S3 i8080 LCD](https://docs.espressif.com/projects/esp-idf/en/v5.5.4/esp32s3/api-reference/peripherals/lcd/i80_lcd.html):8/16-bit DMA bus and memory constraints.
- [ESP-IDF5.5.4 ADC oneshot](https://docs.espressif.com/projects/esp-idf/en/v5.5.4/esp32s3/api-reference/peripherals/adc_oneshot.html):ADC2/Wi-Fi sharing prompted GPIO5CC2 correction.
- [LVGL9.4 display setup](https://lvgl.io/docs/open/9.4/details/main-modules/display/setup):partial/double-buffer rendering and asynchronous flush completion.
- [Freerouting official CLI](https://github.com/freerouting/freerouting/blob/master/doc/command_line_arguments.md) and [settings](https://github.com/freerouting/freerouting/blob/master/doc/settings.md):local headless routing, disabled analytics/API/MCP servers. Official2.5.0 jar SHA256:F6F51BB02245E8E717F9359BD260CC9C5C0B1BC0ACC8B7CB2CD5B8FFEB5DE3C7. Autorouting was followed by native KiCad DRC and manual geometric corrections; router completion alone was never used as approval.
- [JLCPCB manufacturing capabilities](https://jlcpcb.com/capabilities/pcb-capabilities):common prototype4-layer process. This candidate uses0.20 mm minimum tracks/clearance,0.60/0.30 mm vias and0.30 mm edge clearance. The fabricator has not accepted an exact stackup/impedance specification.

BOM quoted subtotals are EUR6.705 and USD47.85 across only5 priced rows;79 rows have no qualified price. No currency conversion, tax/import/shipping, carrier PCB/assembly/enclosure/memory-card costs or false grand total are included. Important components need live EU-accessible stock and a complete procurement quote before order.
''')
write('DESIGN_REVIEW_REVA.md','''# Hostile design review — DO NOT ORDER

The board is a real native KiCad candidate, not a released Rev A. KiCad10.0.1 final ERC reports0 violations; final DRC reports0 violations,0 unconnected items and0 schematic parity issues. Reports are in validation/erc-final.json and validation/drc-final.json. They do not prove analog, firmware, acoustic, mechanical or protection behavior. No physical board was built or tested.

## Defects fixed before final checks

1. Removed octal-PSRAM reserved module GPIOs from application assignments; retained safe boot/reset and default-off peripheral rail control.
2. Corrected the USB shell pad mapping to native SH and tied shield to ground; corrected symbol/PCB parent identifiers and actual NC-net names so parity is clean.
3. Corrected legitimate power-source flags and schematic pin-grid placement; ERC moved from370 findings to0 without exclusions.
4. Replaced the ambiguous older inductor selection with exactSRN6028C-3R9M; corrected microSD to the3V-only Adafruit4682 breakout.
5. Corrected stereo SD networks for the actual breakout's1 MOhm pull-up plus IC pull-down:82 kOhm left,560 kOhm right to switched5V.
6. Moved CC2 from GPIO14ADC2 to GPIO5ADC1 and LCD_D1 to GPIO14; avoids the documented Wi-Fi/ADC2 conflict. Rerouted and checked parity afterward.
7. Repaired overlapping placement/courtyards, unrouted signals, thin0.15 mm router fanouts, remaining power-plane islands, drill-to-drill collisions and a localCC2/LCD_D7 clearance issue.
8. Moved22 routing vias out of SMD component pads; fixed remaining silkscreen collisions while preserving meaningful labels and native component values. Native module thermal-ground construction is a separate audit item.
9. Added proper plane stitching/fanouts so final native connectivity reports0 unconnected items. Rerun after all edits and export from that checked board.

## Five mandatory release gates

| Gate | Finding and why order is blocked | Required closure |
|---|---|---|
|1 Display/harness |Panel datasheet/schematic access-gated; module controller,8-bit mode straps,mating pitch/orientation,brightness/backlight current and timing not verified. CandidateJ2 is not a qualified direct mate. |Obtain full current panel documents/sample, approve cable drawing or substitute a fully documented module, verify voltage/current/timing/power-off behavior and revise schematic/BOM/layout.|
|2 USB power/protection |No qualified VBUSOVP/surge/reverse path or hardware current limiting. TwoRd resistors and ADC taps do not implement source-current handling; unpowered ADC injection is not isolated. TPS22918 input2 A rating leaves inadequate contingency margin. |Redesign input with a documented higher-margin protected/current-limited path and robust CC detection/boot current policy; qualify source orientations/default/1.5 A/3 A, attach/detach,inrush,surge and thermal conditions.|
|3 Powered-off peripherals |Display reset/I2C/data and amplifier I2S/SD may back-power switched rails. Default-off rail gates do not electrically isolate I/O. Required sequencing firmware is absent. |Prove allowed injection under every state or add appropriate isolation/retain rail architecture; implement sequencing and validate worst-case boot/reset/shutdown.|
|4 Footprints/mechanics/procurement |Exact manufacturer land-pattern overlays are incomplete; newer inductor/native footprint match,USB setback,display/harness,pin1,caps/fuse/switch/header configurations unapproved.79BOM rows unpriced; regional stock contradictory. |Complete each FOOTPRINT_AUDIT row with revision/page/overlay; approve harness/mechanical drawings and live supplier quote. Resolve zero-ohm resistor MPN and MLCC effective capacitance.|
|5 Layout/performance evidence |Autorouted candidate has no controlled90 Ohm USB pair validation, no signed stackup, no transient/thermal/audio/RF/combined-load measurements. |Review/rework critical USB/buck/power routing with confirmed stackup; validate prototype using TEST_PLAN after earlier gates permit ordering; no claim of premium UI/audio performance until measured.|

These are unresolved engineering defects/uncertainties, not accepted waivers. The design must change before manufacture. Reporting0ERC/DRC does not satisfy the user's definition of done while these gates remain.

## Detailed subsystem findings

Power: nominal3V3 fixed buck topology and pinout checked; estimated1.162 A3V3 load fits2 A buck on paper. Effective ceramic capacitance,inductor pad fit,thermal derating and actual load transients remain unverified. Input full-power estimate~8 W plus25% contingency~10–10.3 W; nominal3 A supply capacity is enough,2 A input switch margin is not. Capacitor slew calculations alone cannot establish USB startup compliance. No battery hazards were introduced.

Processor: safe NC/boot policy,module flash/PSRAM exact variant and USB/UART recovery provided. Firmware buffering,USB current gating,display driver,touch driver/audio/mic bit alignment not implemented. GPIO matrix allowsLCD_D1 remap; CC usesADC1. ADC ladder loses rollover and released reading can saturate; this is a documented functional limit.

Display: publicNXP host pin map is evidence for signal roles, not panel supply/backlight/mate/timing approval. J2 groundsCS and tiesRD high forwrite-only operation. Mode,straps and display reset while rail off are hard gates.30FPS is a workload target;60 full frames/s is not promised.

Audio: genuineI2S/stereo class-D path with8 Ohm2 W drivers;1.4 W/channel clean-output target. NominalSD voltages computed, tolerances/gain/breakout revision need bench approval. No grounded bridge outputs. Pop/EMI/loopback and AEC are not qualified; push-to-talk half-duplex is theRevA operating concept.

Microphone: top/front remote bottom-port breakout is mechanically plausible; clock/supply guide checked. FullKnowles acoustic/package review,bit alignment,cable reflections and speaker feedback require evidence. Keep foam aperture clear and no adhesive on port.

USB: two5.1 kOhmRd,22 Ohm data resistors,CC/data ESD,PTC and shell ground exist. Native route lengths:DM63.498+connector-side22.670=86.168 mm;DP56.585+27.599=84.184 mm,approx1.984 mm aggregate mismatch. These are geometric totals, not a controlled coupled-pair/skew/impedance qualification. Review pair topology,return path and ESD stub positions; no USB compliance claim.

RF: module RF socket plus real50 OhmTaoglas coax/antenna removes a carrier RF trace/matching requirement. Certification antenna type/gain remains unapproved; current antenna gain up to3 dBi differs from older2.3 dBi documentation. Socket strain relief,cable gender/bend radius/enclosure ground proximity require mechanical proof.

Mechanical: carrier100 x90 mm is actual; final pear enclosure dimensions not determined from incomplete module drawings. Buttons are lower right,mic header top,USBbottom,debug accessible. Headered offboard modules need real keyed/marked harness drawings; generic2.54 mm carrier pins are not mating approval.

Manufacturing: tracks >=0.20 mm,clearance>=0.20 mm,routing vias0.60/0.30 mm,common4-layer proposal.164 routing vias and97 physical footprints in current board; tracks on outer layers only. Inner planes are filled. Some main-power pad neckdowns are0.48–0.601 mm rather than0.8 mm; current/thermal review needs actual lengths/copper thickness,not class-name assurances. SW_NODE total route length~10.669 mm requires buck hot-loop/layout review and likely further compaction before release.0.2 mm3V3 ground/power fanouts are not high-current trunk approval. Module thermal drills/tenting need solderability review.

Debug: realrail/bus pads,EN/BOOT switches,UART andUSBserial/JTAG support dead-firmware recovery. No four-wire externalJTAG becauseSD occupies39–42. Debug3V3 is reference only; external power injection is not protected.

## Native check settings and exports

No custom ERC exclusions or DRC exclusions were added. The JSON reports list native default ignored checks (missing courtyard,via endpoint centering,tuning profiles,footprint filters/component type). Those defaults are not declarations that their subjects are proven; footprint/mechanical audit remains independent. Final error/warning checks found none under the recorded configuration. Minimum rules were not reduced to hide router defects.

Native exports:11-page schematicPDF,PCB layerPDF,3DPNG,11Gerber layers+job file,PTH/NPTHExcellon and maps,positionCSV andBOMCSV.3D rendering succeeded but the installed library lacks ESP32-S3-WROOM-1U.step,so the processor appears as footprint only; no substitute model was invented. Offboard display/amps/mic/speakers/coax are not modeled.3D rendering is visualization,not enclosure fit verification.

Order status: **DO NOT ORDER**. Manufacturing files are review exports only. Completing their generation does not authorize purchase or constitute assembly-ready certification. Review-bundle manifest hashes identify the exact delivered files; any design edit invalidates current checks/exports.
''')
readme='''# NEXUS PEAR REV A — DO NOT ORDER

Actual editable KiCad10.0.1 engineering candidate with hierarchical schematic,fully connected routed4-layer PCB,local symbol/footprint snapshots,BOM,review fabrication exports and engineering documentation. It is not released for manufacture. Critical display/USB power/footprint/layout qualification gates remain in [design review](docs/DESIGN_REVIEW_REVA.md).

| Item | Candidate |
|---|---|
| Processor |ESP32-S3-WROOM-1U-N16R8,16 MBflash/8 MBPSRAM|
| Display |NXP LCD-PAR-S035,3.5-inch IPS,parallel8-bit8080; detailed module qualification incomplete|
| Resolution/touch |480 x320,capacitive5-point candidate|
| Microphone |Adafruit3421/SPH0645LM4H I2S MEMS breakout,top/front|
| Audio/speakers |2xAdafruit3006/MAX98357A stereo selection;2xVisaton2945,8 Ohm/2 W,~1.4 W clean/channel target|
| Networking |2.4 GHzWi-Fi+BLE;realU.FL/coax toTaoglasGW.11.A153 externalantenna|
| Storage |16 MBmoduleflash,8 MBPSRAM;Adafruit4682microSD breakout|
| PCB |4layers,100 x90 mm,97physicalfootprints,164routingvias|
| USB |USB-C5 Vinput andUSB2.0FSdevice serial/JTAG;noPD/host|
| Estimated power |~8 Wpeakload estimate;~10–10.3 Wwithcontingency;~2.6 Wtypical scenario,notmeasured|
| BOM |84rows;only5priced,EUR6.705+USD47.85separate quotedsubtotals;79unpriced,notacompleteestimate|
| ERC |0violations inerc-final.json|
| DRC |0violations,0unconnected,0schematicparityissues indrc-final.json|

## Open and review

- [KiCad project](hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pro),[schematic](hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_sch),[PCB](hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pcb). LocalNexus.pretty,Nexus.kicad_sym and librarytables accompany them.
- [BOM_REVA.csv](hardware/BOM_REVA.csv):exactcandidateMPNs,availability/source notes,blankunverified prices;excludes fabrication/assembly/enclosure/card quote.
- [Manufacturing review exports](hardware/manufacturing/DO_NOT_ORDER.md):gerbers/,drill/,position/,bom/.These are intentionally marked nonrelease and must not be uploaded for manufacture.
- [SchematicPDF](previews/schematic.pdf),[PCBlayerPDF](previews/pcb-layers.pdf),[3Drender](previews/board-3d.png). Installedprocessor3Dmodel ismissing;processor footprintisvisible. Offboardpartsnotmodeled.
- [Architecture](docs/ARCHITECTURE.md),[processor decision](docs/PROCESSOR_DECISION.md),[display](docs/DISPLAY_RESEARCH.md),[audio](docs/AUDIO_DESIGN.md),[powerbudget](docs/POWER_BUDGET.md),[pins](docs/PIN_ASSIGNMENTS.md),[footprintaudit](docs/FOOTPRINT_AUDIT.md),[testplan](docs/TEST_PLAN_REVA.md),[sources](docs/SOURCES.md),[hostilereview](docs/DESIGN_REVIEW_REVA.md).
- validation/ containsfinalnativeJSONreports,iterationhistory,footprintpadinventory,layoutmetrics,BOMsummary anddeliverymanifest. Intermediatefailuresarekeptfortraceability;onlyfinalreportsdescribe deliveredboard.

## What must change before order

1. Obtain/display datasheet anddrawing;approvecontroller,mode,mate,cable,current andtiming.
2. Redesign/qualifyUSBVBUSprotection,currentpermission/unpoweredCCandinputcurrentmargin.
3. Eliminatepowered-offdisplay/audioI/Oinjection andimplementverifiedsequencing.
4. Completeeverymanufacturerfootprint/mechanicaloverlay,harnessdrawing andliveprocurementquote.
5. ReviewcriticalUSB/buck/powerrouting againstsignedstackup,thenrerunchecks/regenerateexports;performbring-upafterearliergatespermitprototypeorder.

No physicalboard,firmware,thermal/acoustic/EMItest orenclosurefit hasbeenvalidated. ThisworkmakesRevBdevelopmentconcrete butdoesnotsatisfythefullreleasedRevAdefinitionofdone.
'''
# Restore readable spaces in compact automated README text through a separately authored final overwrite below.
(out/'README.md').write_text(readme,encoding='utf8')
m=out/'hardware/manufacturing';(m/'DO_NOT_ORDER.md').write_text('''# DO NOT ORDER — review exports only

These Gerbers, drills, positions and BOM were generated from the checked candidate. Native ERC/DRC pass, but display/harness qualification, USB source-current/protection redesign, powered-off I/O isolation, full footprint audits and critical layout review remain unresolved. Read ../../docs/DESIGN_REVIEW_REVA.md before any fabrication decision.

Proposed 4 layers: F.Cu, In1.Cu ground, In2.Cu 3V3, B.Cu. Proposed common 1.6 mm board, outer1 oz/inner0.5 oz, ordinary prototype process. This is NOT a fabricator-approved stackup or impedance specification. Position CSV is in mm with KiCad absolute-origin convention; rotations and PTH/manual parts need assembly-house review. All referenced carrier parts are top-side. No assembly contract or panelization is approved.

Export timestamp and hashes are in ../../validation/delivery-manifest.json. Any PCB edit requires fresh zone refill, ERC/DRC/parity review and regenerated outputs. Do not order from this directory.
''',encoding='utf8')
print('Created sources, hostile review, README and manufacturing release warning')
