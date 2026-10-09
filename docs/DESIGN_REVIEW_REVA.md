# The pear is on trial — final design review

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

Final native checks: ERC 0, DRC 0, unconnected 0, schematic parity 0. The checked revision contains 117 physical footprints. Procurement remains incomplete: 96 of 106 BOM rows are unpriced. RFQ_GROUPED.csv is a draft procurement input, not a supplier commitment. Missing 3D component bodies are listed in FINAL_CHECK.md.
