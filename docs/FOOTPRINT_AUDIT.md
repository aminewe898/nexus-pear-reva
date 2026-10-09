# Trust issues, measured in millimeters — footprint audit

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
