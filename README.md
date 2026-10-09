# NEXUS PEAR REV A — pear pressure

**DO NOT ORDER — engineering review submission.** Revised project: 2026-10-07.

ESP32-S3-WROOM-1U-N16R8, 16 MB flash/8 MB PSRAM, Waveshare 29318 IPS touch display (320 x 480 native / 480 x 320 landscape), two-point FT6336U, digital I2S microphone, stereo MAX98357A modules, 8-ohm speakers, optional microSD, real U.FL-to-RP-SMA external antenna, six ADC keys and bottom USB-C. Carrier 100 x 90 mm, four layers, no battery. Design peak allowance 11.54 W including 20% contingency and an enforced 0.75 W/channel audio cap; no measured peak is claimed.

Open hardware/kicad/nexus-pear-reva/nexus-pear-reva.kicad_pro in KiCad 10. Native schematic, PCB, local symbols and local footprints are included. previews/schematic.pdf is the complete eleven-sheet schematic; previews/pcb-layers.pdf and board-3d.png support review. Manufacturing Gerbers, Excellon drill files, placement CSV, BOM and STEP are under hardware/manufacturing/. Do not submit those as an approved fabrication order.

hardware/BOM_REVA.csv contains exact candidate MPNs; hardware/RFQ_GROUPED.csv groups quantities for procurement. Pricing is incomplete. SUBMISSION.md is the short cover note; docs/ contains the architecture, processor comparison, display/audio/power calculations, pin map, footprint review, sources and first-article test plan. docs/DESIGN_REVIEW_REVA.md identifies every remaining release gate. Native ERC/DRC reports, pad inventory, route metrics and hashed delivery manifest are under validation/.

The revised circuit adds hardware Type-C current qualification and protected input power, removes independently powered 3.3 V peripherals, isolates audio signals and replaces the undocumented display. Corrected manufacturer footprints and routing are in this project's native files. Firmware, physical qualification, complete procurement and enclosure design remain to be completed.
