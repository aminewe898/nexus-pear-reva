from pathlib import Path
import json
out=Path('outputs/nexus-pear-reva');docs=out/'docs';docs.mkdir(exist_ok=True)
def write(name,s): (docs/name).write_text(s.strip()+'\n',encoding='utf8')
write('ARCHITECTURE.md','''# NEXUS PEAR REV A architecture — DO NOT ORDER

This is an editable electrical and placement/routing candidate, not a released prototype. No hardware has been assembled or measured. Display and cable qualification, protection changes, footprint drawing audits and the final layout review remain mandatory. See DESIGN_REVIEW_REVA.md and the native validation reports.

The processor is ESP32-S3-WROOM-1U-N16R8: 16 MB flash, 8 MB octal PSRAM, Wi-Fi 2.4 GHz and BLE, USB full-speed serial/JTAG, and a real module RF socket. Inference, STT and TTS run on remote services. Firmware handles UI, streaming, TLS, audio buffering, buttons and storage. No application firmware is supplied by this hardware task. ESP-IDF 5.5.4 was consulted for peripheral constraints; LVGL 9.4 partial rendering is the proposed UI approach.

```mermaid
flowchart LR
 USB[USB-C 5 V + USB FS] --> P[Fuse / soft-start / buck]
 P --> ESP[ESP32-S3 + flash + PSRAM]
 ESP --> LCD[8-bit 8080 IPS display]
 ESP <-->|I2C| TOUCH[Capacitive touch + expansion]
 MIC[Top I2S microphone] --> ESP
 ESP --> AMP[Two I2S class-D breakout modules]
 AMP --> SPK[Left and right 8-ohm speakers]
 ESP <-->|SPI| SD[microSD breakout]
 ESP <-->|50-ohm coax| ANT[External 2.4 GHz antenna]
 ESP <-->|Wi-Fi| NET[AI / homelab / music services]
 KEYS[Six ADC ladder buttons] --> ESP
```

Audio, microphone, storage and display are modular harness-connected assemblies. The carrier headers have explicitly defined pin orders; they are NOT promises of direct physical compatibility with breakout headers. Only approved point-to-point harnesses may be attached. The microphone goes near the enclosure top; the two amplifiers/speakers occupy the lower left/right. The normal rectangular display occupies the upper front. Buttons occupy the carrier's lower right. USB exits the bottom; reset/boot, UART and expansion remain accessible.

The actual carrier is 100 x 90 mm, with four mounting holes. This is an engineering board dimension, not a measured final pear enclosure. The board rectangle preserves debugging access. Final enclosure size cannot responsibly be derived until the display drawing and all harness/mechanical envelopes are verified. Antenna GW.11.A153 is approximately 84.4 x 7.8 mm and the chosen speaker drivers are 28 x 40 mm; actual installed clearances require CAD review.

Four layers were selected because the 8-bit display, USB, Wi-Fi module supply, I2S and buck require dependable returns. Two layers would impose more crossed routes and broken ground paths. Proposed common 1.6 mm stack: outer signal/copper, inner ground, inner 3V3, outer signal. Outer 1 oz/inner 0.5 oz are a proposed fab choice, not a signed stackup. Inner rail plane and ground connections must pass native connectivity checks. Switching node copper must remain compact and clear of signal routes/planes where appropriate. USB impedance and return continuity are not qualified by ordinary clearance DRC.

Rev A deliberately omits battery, charger, bare-chip RF, PWM audio, eMMC, USB-PD and USB host. It uses minimal status indication and one 3.3 V I2C expansion header. Onboard flash serves firmware/configuration; microSD serves music/assets/logs. External debug 3V3 is a reference only and must never back-power the USB supply.
''')
write('PROCESSOR_DECISION.md','''# Processor decision

Decision: ESP32-S3-WROOM-1U-N16R8 for a 480 x 320 IPS parallel display and remote AI. This decision is contingent on display qualification and a measured combined UI/audio/Wi-Fi benchmark. The architecture does not promise 60 FPS full-screen animation.

| Option | Memory and display | Network/audio/USB | PCB, cost and maintainability judgment |
|---|---|---|---|
| ESP32-S3 module, selected | 16 MB flash + 8 MB PSRAM; 8-bit i8080 DMA; 480 x 320 partial UI is realistic | Wi-Fi + BLE integrated; independent I2S RX/TX; USB FS serial/JTAG | Castellated module avoids BGA and RF design. Mature ESP-IDF/LVGL path, fast MCU boot. Module listing EUR5.94 at DigiKey Spain but zero stock at research; alternate Mouser stock listing requires live confirmation. Lowest suitable integration burden. |
| ESP32-P4 ecosystem | Stronger display engine; MIPI DSI/CSI, larger external PSRAM; 800 x 480 or above attractive | P4 needs a separate wireless device; reference function board uses C6. Rich audio interfaces, USB FS/HS | Better premium full-frame UI margin but extra wireless link, high-density processor and display infrastructure raise Rev A complexity/power/cost. Revisit if S3 bandwidth benchmark fails. Reference board is not a drop-in 3.5-inch product. |
| STM32H743 class | 480 MHz M7, up to 2 MB flash/1 MB RAM; LTDC with external framebuffer memory | SAI/I2S, USB; external Wi-Fi/BLE needed | Good real-time display/audio platform; SDRAM plus wireless plus controller/package routing burden and fragmented application integration exceed the chosen module. No inherent advantage for remote AI. |
| RP2350 | Dual 150 MHz M33/RISC-V options, 520 KB internal RAM; external PSRAM possible; PIO/HSTX | External Wi-Fi required; PIO/I2S work needed; USB device | Strong low-cost MCU but this combination consumes peripherals and engineering time. Full double RGB565 framebuffer already exceeds internal RAM. Not the lowest-risk premium network/audio terminal. |
| Raspberry Pi Zero 2 W / small Linux SBC | 512 MB RAM; Linux graphics and codecs; HDMI display adaptation rather than native DSI on Zero 2 W | Wi-Fi/Bluetooth, USB, I2S peripherals possible | Easier rich application stack, but OS boot, SD integrity, power and HDMI adapter/mechanical overhead. Separate compute module carrier increases integration work. Local AI is not required, so Linux is not selected by default. |

Prices for unselected architectures are not a current procurement quote. Exact comparative wattage and boot time depend on firmware, modules and peripherals; no synthetic bench numbers are claimed. P4 is the strongest upgrade path for 800 x 480 at sustained full-frame rates. S3 needs a partial-render UI, bounded audio buffers and priority isolation so TLS/network activity cannot starve audio DMA.

The S3 module datasheet pin table was cross-checked. GPIO35/36/37 are reserved for octal PSRAM and left unconnected; strap pins 3/45/46 are also left unused. GPIO0 has a pull-up and a boot switch; EN has 10 kOhm/1 uF reset conditioning and reset switch. Native USB uses GPIO19/20. Crystal and flash/PSRAM wiring are inside the module. GPIO5 now senses CC2 with ADC1; the earlier GPIO14 ADC2 assignment was corrected because Wi-Fi shares ADC2. See the generated pin table.

Release benchmark: concurrent 48 kHz stereo playback, mic capture, Wi-Fi/TLS streaming and LVGL UI must show no underruns over 30 minutes. Start display WR at 5 MHz, then raise only within actual panel timing limits; target 30 FPS on the defined UI workload, not unconditional full-screen animation. If the verified display cannot support this, adopt a documented alternative or P4 architecture before manufacture.
''')
write('DISPLAY_RESEARCH.md','''# Display research — selection provisional

Primary: **NXP LCD-PAR-S035**, 3.5-inch rectangular IPS, 480 x 320, capacitive five-point touch, parallel 8080/SPI interface. NXP's product page listed USD29 and more than 100 units at research. Public AN14776 and UM12018 establish the parallel connector signal functions and 3.3 V host interface. Detailed display datasheet/schematic downloads require an account and were not obtained. Therefore controller identity (often reported as ILI9488), mode straps, backlight draw, exact mechanical connector, brightness, contrast and maximum WR timing are NOT released facts. J2 is a candidate 2x14 2.54 mm carrier header, not a verified direct mate.

Alternative 1: **Waveshare 3.5inch Capacitive Touch LCD, SKU29318**, IPS 320 x 480, ST7796S and FT6336U, SPI. Product page listed USD18.99 and in stock. Simpler interface and more public documentation, but quoted controller timing of 66 ns SPI clock period implies approximately 15.15 Mbit/s, only 6.16 RGB565 full frames/s before overhead. Partial UIs remain possible; smooth full-frame motion needs qualification. Do not rely on an example overclock as guaranteed panel timing.

Alternative 2: **BuyDisplay ER-TFT035IPS-6-4405**, 3.5-inch 320 x 480 IPS, candidate parallel ILI9488 and optional FT6236 touch. Manufacturer datasheet endpoint returned HTTP403. Exact touch-option MPN, mechanical drawing and stock/price were not verified. This remains an alternative to investigate, not an approved substitution.

| 480 x 320 | RGB565 | RGB888 |
|---|---:|---:|
| Single framebuffer | 307,200 B = 300 KiB | 460,800 B = 450 KiB |
| Double framebuffer | 614,400 B = 600 KiB | 921,600 B = 900 KiB |
| 30 FPS payload | 9.216 MB/s = 73.728 Mbit/s | 13.824 MB/s = 110.592 Mbit/s |
| 60 FPS payload | 18.432 MB/s = 147.456 Mbit/s | 27.648 MB/s = 221.184 Mbit/s |

These are uncompressed pixel payloads excluding commands, blanking and bus stalls. They do not assert panel support for both color modes. An 8-bit 20 MHz i8080 bus has 20 MB/s ideal capacity: 65.1 RGB565 frames/s ideally; 30 FPS needs 46.1% utilization, 60 needs 92.2%. Real DMA/PSRAM contention, setup/hold and controller command overhead make 60 FPS an unsuitable promise. Twenty MHz is a proposed benchmark target, NOT a verified panel limit. Two partial draw buffers of roughly 30 KiB each are a reasonable LVGL starting point; flush completion must follow DMA completion. The 8 MB PSRAM can hold full double buffers but not eliminate bandwidth contention.

800 x 480: RGB565 single 768,000 B/750 KiB, double 1,536,000 B; RGB888 single 1,152,000 B/1,125 KiB, double 2,304,000 B. At 30 FPS these need 23.04 MB/s and 34.56 MB/s respectively. An 8-bit 20 MHz bus cannot deliver even the RGB565 full-frame payload at 30 FPS. Thus 800 x 480 is not forced onto this architecture.

SPI trades pin count for bandwidth; QSPI could improve it only with a documented supporting panel/controller and driver. Parallel i8080 gives a usable 8-bit DMA path without a continuous RGB framebuffer scan. RGB parallel needs many pins, blanking timing and predictable framebuffer access. MIPI DSI is a stronger P4-class upgrade but not a native S3 interface. No AMOLED panel with adequately verified small-module integration was found in this research; IPS is selected provisionally.

J2 carrier mapping: 1 switched3V3, 2 GND, 3 SCL, 4 SDA, 5 touch IRQ unused/polled, 6 backlight control tied switched3V3, 7 reset, 8 DC, 9 CS grounded, 10 WR, 11 RD tied switched3V3, 12 TE unused, 13–20 D0–D7, 21–28 unused. Reset comes from EN through 100 Ohm. The public NXP host manual/application note supports this signal map, but the panel's 8-bit-mode strap and powered-off injection must be verified. Backlight tied high also means brightness PWM is not implemented. Verify whether pin6 is control rather than direct LED power before attaching anything.

Mandatory before order: obtain panel drawing/datasheet, verify its exact sales revision and controller, compare mating connector pitch/orientation against J2 or replace J2 with a verified harness, establish backlight current and logic limits, define mode straps, measure signal integrity and check reset/I2C/display-pin back-power when its rail is off. Final enclosure dimensions await these drawings.
''')
write('AUDIO_DESIGN.md','''# Audio and microphone

Two **Adafruit3006 MAX98357A** class-D amplifier breakout modules receive one stereo I2S stream and each selects its channel using SD voltage. This keeps tiny amplifier packages and high-current speaker outputs off the carrier for Rev A. Each speaker attaches to its amplifier terminal block. The carrier header order is VIN, GND, SD, GAIN unused, DIN, BCLK, LRCLK; it requires a labeled custom harness. Breakout pin order must be checked before assembly.

Output format: 48 kHz stereo, 32-bit slots, 64 BCLK per frame = 3.072 MHz. Source samples can be 16/24-bit sign extended to 32-bit slots. MAX98357A accepts I2S without MCLK. J3 selects left, J4 right. Adafruit's breakout has a 1 MOhm SD pull-up to VIN plus the IC's nominal 100 kOhm pull-down. R15=82 kOhm to switched5V produces approximately 2.845 V at SD; R16=560 kOhm produces approximately 1.09 V, nominally selecting right. The original 3.3 V/330 kOhm network was corrected during review. Internal pull-down tolerance and actual breakout revision need worst-case/bench validation. GAIN floating corresponds to nominal9 dB; verify installed breakout wiring. Control PERIPH_EN defaults low to gate both amplifiers and display; there is no independently programmable left/right hardware mute.

Speakers: **Visaton2945 K28.40, 8 Ohm, 2 W rated/3 W maximum, 28 x 40 mm**. At 5 V/8 Ohm MAX98357A publishes roughly1.4 W at1% THD and1.8 W at10% THD, so budget/limit approximately1.4 W per channel. This is usable small-device music/TTS, not a claim of3 W clean output per speaker. DSP high-pass near200 Hz and output limiting are proposed starting settings for the small driver; acoustic measurements must set final EQ and limit. No PWM audio.

Class-D outputs are bridge-driven: neither speaker wire goes to ground, neither connects to headphone jack ground, and left/right outputs must never be combined. Short twisted speaker pairs go directly to amplifier terminal blocks away from mic/coax. The breakout uses a filterless class-D topology for short wiring; long speaker cables or failed EMI measurements require a qualified LC/filter redesign. Do not invent ferrite/LC values without checking the amplifier load stability and EMI tests.

Mute/pop sequence: hold PERIPH_EN low and all outgoing bus pins low/high-impedance during boot; establish correct I2S framing and zero samples, enable rails, wait for measured rail settling, ramp software gain over10–20 ms. Ramp down to zero before rail shutdown. Avoid driving unpowered peripherals. This required firmware is NOT supplied or validated here; load switches alone do not isolate I/O. Powered-off injection remains a release gate.

Microphone: **Adafruit3421 SPH0645LM4H I2S MEMS breakout**, supply3.3 V (guide specifies1.6–3.6 V), bottom acoustic port. Shared 48 kHz LRCLK/3.072 MHz BCLK is within the guide's2–4 MHz recommended BCLK range. Mic DOUT is independent of amp DIN; SEL grounded selects one slot. Capture into32-bit slots and verify actual bit alignment/sign with the Knowles datasheet and test signal. Downsample with a real anti-alias filter to16 kHz mono for STT; do not just discard samples. Breakout supply decoupling is onboard; verify exact board revision and cable rail stability.

Mount the microphone breakout near the enclosure top/front with its PCB acoustic opening facing a short external aperture. A foam gasket seals that aperture against enclosure air pressure from the speakers; do not cover the hole with adhesive or put a screw/solid wall behind it. The MEMS package is on the opposite side of a bottom-port PCB opening. Keep speaker vents mechanically separated and avoid a long shared acoustic duct. Approximately100 mm microphone harness is a proposed limit requiring signal integrity and noise checks, not a characterized maximum.

Rev A uses push-to-talk and half-duplex capture/playback. Always-listening full-duplex voice with acoustic echo cancellation is not implemented or proven. Test speaker-to-mic coupling and gain limits before enabling simultaneous voice interaction. Full Knowles package/acoustic datasheet review remains incomplete; the purchased breakout reduces assembly burden but does not remove the need to verify its documentation.
''')
write('POWER_BUDGET.md','''# Power budget and release gaps

No battery. Nominal source: USB-C5 V/3 A only after valid current advertisement. The connector's aggregate5 A rating does not establish source current permission. A PC USB port may supply much less. No USB-PD or host mode is implemented.

| Load | Peak assumption | Power |
|---|---:|---:|
| ESP32-S3/module | 600 mA at3.3 V |1.980 W|
| Display/backlight/touch |350 mA at3.3 V, UNVERIFIED |1.155 W|
| microSD |200 mA at3.3 V, transient allowance |0.660 W|
| Mic |2 mA at3.3 V |0.0066 W|
| LED/ladder/I2C/peripherals |10 mA at3.3 V |0.033 W|
| Total3V3 |1.162 A |3.8346 W|
| Buck input at85% efficiency | — |4.511 W|
| Two speakers,1.4 W each,85% amp efficiency | — |3.294 W|
| Amp quiescent/switch/cable/misc allowance | — |about0.2 W|
| Estimated input peak |about1.60 A at5 V |about8.0 W|
| 25% contingency |about2.0–2.1 A at5 V |about10.0–10.3 W|

At nominal5 V, a genuinely advertised3 A supply has15 W available and is sufficient for this estimate. The board's input **TPS22918 is rated2 A continuous**, so the contingency sits at/exceeds its rating and leaves inadequate derated margin. Replace/qualify that input path before release; a3 A PTC is not a current limiter. At4.4 V the same8 W load needs~1.82 A before additional loss. Audio output drops with voltage, but fixed-load/thermal margin still needs measurement. Display current is not a measured or verified datasheet value, so the estimate cannot close the power gate.

Typical example: module150 mA + display180 mA + SD30 mA + other12 mA =372 mA at3.3 V,1.228 W; at90% buck efficiency1.364 W. Music averaging1 W total acoustic electrical drive at85% amplifier efficiency adds1.176 W. Misc~0.06 W gives~2.6 W typical. Idle/audio-off might be1–2 W depending on backlight/Wi-Fi state. These are scenarios, not bench results.

Path: USB VBUS -> MF-MSMF300/16X-2 PTC -> always-enabled TPS22918DBVR soft-start ->5V rail. AP63203WU-7 synchronous buck generates3V3;3.9 uH BournsSRN6028C-3R9M,100 nF bootstrap,10 uF input,2x22 uF output. U6 gates5V_AUDIO and U7 gates3V3_DISPLAY. TPS22918 pins were checked:1 VIN,2 GND,3 ON,4 CT,5 QOD (unused),6 VOUT. AP63203 pins checked:1 FB,2 EN,3 VIN,4 GND,5 SW,6 BST. Buck FB is tied to3V3 for the fixed-output device, EN to its input. TPS22918 QOD is unused: rails decay by load rather than a specified discharge profile.

Bourns inductor official row gives3.3 A RMS,3.9 A saturation and nominal28 mOhm DCR with20% inductance tolerance. This is the **C** series exact MPN, not the older part. Buck2 A rating exceeds estimated3V3 demand; transient, saturation, temperature and layout qualification remain required. Ceramic DC-bias effective capacitance is unverified for the exact Murata selections. Loss estimates: at85% buck efficiency~0.68 W conversion loss at peak; roughly0.08 Ohm typical input-switch resistance at1.6 A gives0.205 W, but typical resistance is not worst-case thermal signoff. Use actual datasheet maximum attemperature and verify junction rise.

Inrush:4.7 uF nominal precedes the input switch; tolerance plus connector/ESD parasitics must stay within applicable USB sink input-capacitance limits. CT=10 nF gives datasheet nominal slew parameter0.55*CT(pF)+30 microseconds/V =5530 microseconds/V, approximately27.65 ms5 V rise. A10 uF downstream capacitor alone then charges at~1.81 mA. This is NOT the full startup current: buck startup, output capacitors, load steps and attached breakout capacitors are reflected at input. Default USB100 mA startup cannot be guaranteed with present hardware/firmware. Display/audio default off helps, but module boot and radio must obey current permission.

Critical missing protection: there is no dedicated VBUS surge TVS/OVP/reverse isolation. USBLC6 protects data/CC ESD but does not guarantee the TPS22918's6 V absolute maximum against VBUS surges. CC sensing through22 kOhm plus4.7 nF filters does not provide unpowered ADC isolation or a certified sink controller. Both CC inputs now use ADC1; current classification/calibration firmware is absent. Hardware current-limited VBUS/OVP with proper thresholds and supported CC detection should replace this candidate path. Also isolate/reset or retain power appropriately to eliminate display/audio I/O back-power. The budget and these gates require DO NOT ORDER.
''')
# Automated exact pin table from canonical design data.
data=json.loads((out/'design_data.json').read_text())['parts'];u=next(d for d in data if d['ref']=='U1')
s='# Pin assignments — canonical schematic mapping\n\nBoth CC sensors use ADC1 (GPIO2/GPIO5). GPIO14 drives LCD_D1. This corrects the Wi-Fi/ADC2 conflict found in self-review.\n\n| Module pad | Module signal | Carrier net |\n|---|---|---|\n'
for x in u['pins']:s+=f"|{x['num']}|{x['name']}|{x['net'] or 'NC'}|\n"
s+='\n## Connectors\n\nHeaders are carrier harness assignments, not direct breakout mating guarantees. Pin1 must be identified on both cable ends, with a continuity-tested drawing.\n'
for d in data:
 if d['ref'].startswith('J'):
  s+=f"\n### {d['ref']} — {d['value']}\n\n| Pad | Net |\n|---|---|\n"
  for x in d['pins']:s+=f"|{x['num']}|{x['net'] or 'NC'}|\n"
s+='''\n## Buttons and debug

GPIO1 ADC1 has10 kOhm to3V3. UP0 Ohm, DOWN1 kOhm, LEFT2.2 kOhm, RIGHT4.7 kOhm, OK10 kOhm, BACK22 kOhm to ground produce nominal0,0.300,0.595,1.055,1.650,2.269 V; released approaches3.3 V and may saturate the ADC. Select attenuation and calibrate thresholds; released >2.8 V is a proposed threshold. Poll200 Hz with20–25 ms stable debounce. Simultaneous buttons can alias a valid code; this design supports single-button use, not guaranteed rollover. Test-point KEY_ADC permits calibration. If rollover is required use an expander/dedicated pins in Rev B.

BOOT/RESET are separate switches. UART header includes ground/TX/RX/EN/BOOT/reference3V3. USB serial/JTAG is the preferred programming/debug path; GPIO39–42 are used by SD and are not available as an external four-wire JTAG port. Testpoints use actual1 mm pad footprints for rails and important buses; the PCB labels map to their schematic nets. Expansion provides3V3/GND/SCL/SDA; combined pull-ups/capacitance and external ESD must be checked for the installed accessory. No external cable ESD certification is claimed.
'''
write('PIN_ASSIGNMENTS.md',s)
write('FOOTPRINT_AUDIT.md','''# Footprint audit — incomplete, order prohibited

Native KiCad10.0.1 footprints were copied into project-local Nexus.pretty; the project is not dependent on future library geometry changes. Local symbol pins have explicit numbers/electrical types. validation/footprint-pad-inventory.json records actual footprint pads/nets; it establishes symbol/PCB mapping, not manufacturer mechanical approval. No undocumented dimensions were invented. A library footprint existing is not evidence of approval.

| Part / footprint | Electrical/pin check | Mechanical/land-pattern status |
|---|---|---|
| ESP32-S3-WROOM-1U-N16R8 / ESP32-S3-WROOM-1U |41 module pads compared to official pin table; reserved PSRAM pins NC |Library module outline/pads snapshot; full dimensional/orientation/underside-ground comparison not signed off. Local thermal via drills changed0.2 to0.3 mm with0.6 mm diameter for conservative fabrication; solder-wicking/tenting and module grounding need review.|
| GCTUSB4105-GF-A / native USB-C16-pin USB4105 |A/B USB pairs, CC1/2, shield checked; actual native SH pad recognized and bonded GND |Official drawing downloaded in research. Full pad-coordinate comparison, shell stakes, board-edge setback and plug overhang not signed off.|
| TPS22918DBVR / SOT-23-6 |1 VIN/2 GND/3 ON/4 CT/5 QOD/6 VOUT checked against TI |DBV package and pin1 convention selected; pitch/pad dimensions versus recommended land pattern not signed off.|
| AP63203WU-7 / TSOT-23-6 |1 FB/2 EN/3 VIN/4 GND/5 SW/6 BST checked |TSOT footprint selected; complete land-pattern/orientation comparison pending.|
| USBLC6-2SC6 / SOT-23-6 |IO1 pins1/6,IO2 pins3/4,GND2,VBUS5 checked |SC6 package matched by name; complete physical drawing audit pending.|
| SRN6028C-3R9M / native SRN6028 |Correct C-series electrical specification selected |Footprint originally named older series; exact C-series dimensions/pads must be compared. Not approved by similar name.|
| MF-MSMF300/16X-2 /1812 fuse |Exact MPN selected |Body/terminal/pad and temperature derating audit incomplete.|
| Samtec TSW headers /2.54 mm vertical |All carrier pin orders explicit |Exact post length/plating,2x14 LCD mating geometry and harness polarity require drawings; no direct breakout fit claimed.|
| OmronB3F1000 /SW_PUSH_6mm |Duplicate1/1 and2/2 pads recognized, two contacts correct |6 mm library footprint selected; actuator height, lead spacing, hole tolerances and enclosure caps pending.|
| Murata MLCC /0805,1206 |Values/nominal voltage exact MPNs populated |Package designation selected; DC bias, tolerance, effective capacitance and land-pattern checks pending.|
| Yageo resistors /0805 |Values selected |Exact special-value MPN spelling, tolerance/availability and pads pending; BOM is not a purchase order.|
| TestPoint_Pad_D1.0mm and mounting holes |Real footprints, measurable rails/signals |Probe access and screw keepout require mechanical inspection.|
| Adafruit3006/3421/4682,Visaton2945,TaoglasGW.11.A153/CAB.774 |Offboard assemblies selected |No carrier footprint for their silicon. Harnesses, speaker polarity, acoustic port, coax gender and mounting are part of the audit and remain incomplete.|

Release procedure for EVERY risky row: obtain current manufacturer package drawing; record revision/page; compare pin1/orientation, pad coordinates/size, pitch, exposed-ground details, solder mask/paste, courtyard, drill/stake/mounting dimensions and board-edge reference; attach a dimensioned overlay and reviewer/date. For headers verify mated view vs PCB view to avoid mirror reversal. Print1:1 and place physical samples as a final supplemental check. Record approval individually; do not convert this table to blanket 'verified' based on ERC/DRC.
''')
write('TEST_PLAN_REVA.md','''# Bring-up checklist — after release gates close

These are planned acceptance tests, not completed results. Do not connect an unqualified display/harness or power this candidate until protection, source-current behavior and routing are fixed. Use current-limited bench power and appropriate instrumentation; breakout module revisions must match harness drawings. Ground-referenced instruments must not short class-D outputs.

| Step | Test | Expected / acceptance |
|---|---|---|
|1|Visual inspection|Correct polarity/MPNs; no bridges; compare assembly drawings; antenna socket/harnesses seated; acoustic hole clear.|
|2|Unpowered resistance|No short on VBUS,5V,3V3,switched rails; caps charge consistently. Record actual values; do not invent a universal resistance cutoff for an MCU rail.|
|3|Limited initial supply|Begin with peripherals absent and100 mA limit; monitor current/voltage. If boot current requires more, characterize safely on bench and redesign USB startup compliance rather than increasing port load blindly.|
|4|5V path|Input/output within source and switch specifications, no excessive drop; characterize inrush and advertised-current/attach/detach states.|
|5|3V3 buck|3.3 V within regulator tolerance and module limits atidle/load; scope ripple/undershoot with short ground spring; no sustained overshoot.|
|6|Reset/boot|EN rises cleanly after rail, reset pulls low, GPIO0 default high; each boot strap confirmed; no power-off injected voltage.|
|7|Programming/recovery|ROM download works by USB and UART; BOOT+RESET recovers a deliberately faulty firmware; read16 MB flash/8 MB PSRAM correctly.|
|8|Status|GPIO48 status toggles; PERIPH_EN remains low until permission; low-current boot mode recorded.|
|9|USB|Enumerate stable FS device, repeated insert/remove, both plug orientations; CC1/2 detection correct including default/1.5 A/3 A sources, unpowered MCU; no excessive source current.|
|10|Display/touch|Verify cable/mode/draw/current before plug-in; all-color patterns correct, reset reliable; five-point touch coordinates/orientation/I2C clock checked; start5 MHz then qualify timing.|
|11|Buttons|Measure each ADC voltage/threshold over supply/temp;20–25 ms debounce; released saturation accepted; document simultaneous-key aliases.|
|12|Storage|Initialize selected3V-only breakout, read/write/checksum test, power interruption behavior and no unexpected bus drive/hotplug corruption; use conservative clock first.|
|13|Microphone|48 kHz/64fs clock, slot and sign correct; known-tone frequency; clean speech capture with Wi-Fi/buck active; no acoustic-port blockage.|
|14|Amplifier|SD thresholds/gain/channel select checked; zero samples then enable; no severe pop, no power-off injection.|
|15|Left speaker|1 kHz left-only signal produces left output; verify8 Ohm driver and clean output limit below1.4 W equivalent into suitable testload.|
|16|Right speaker|Right-only signal produces right output; no mixed-channel selection; compare channel levels.|
|17|Wi-Fi|2.4 GHz scan/connect/reconnect/TLS; streaming without reset; record supply ripple and antenna RSSI at fixed locations.|
|18|Antenna|Correct50 Ohm coax/U.FL/RP-SMA gender, strain relief, gain/certification approval; enclosure orientation test; no mechanical socket load.|
|19|Combined load|30 min UI/audio/Wi-Fi/mic/SD workload, no underruns/resets; monitor peaks against negotiated current; measured frame rate and latency recorded.|
|20|Thermal soak|At worst ambient/enclosure load, monitor regulator/switch/module/amps; temperatures and calculated junctions below datasheet limits with engineering margin.|
|21|Shutdown/back-power|Display/audio off while MCU active, USB removed while debug attached, all signal states: no rail raising beyond component injection limits.|
|22|Mechanical/EMI|USB accessible, buttons aligned, screws clear, microphone gasket sealed, speaker vents free, coax/cables strain-relieved; pre-compliance emissions and ESD plan recorded.|

Archive oscilloscope captures, power measurements, firmware commit/build options, module revisions, actual panel ID, card/antenna/supply models and serial number. A release requires dated evidence against each gate in DESIGN_REVIEW_REVA.md, not merely checkmarks.
''')
print('Created architecture, decision, display/audio/power, pins, footprint audit and test plan')
