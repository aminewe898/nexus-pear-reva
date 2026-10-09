# Screen time, but make it engineering

Selected: Waveshare 3.5inch Capacitive Touch LCD, SKU 29318. Public schematic, pin table and controller datasheets replace the previous account-gated NXP candidate. ST7796S, native 320 x 480 RGB565, rotated to 480 x 320 landscape, IPS, FT6336U two-point touch. Module outline 61 x 92.44 mm; active area 48.96 x 73.44 mm. Manufacturer price observed: USD 18.99, 2026-10-07; shipping and taxes excluded.

Use 3.3 V mode: J2 pins 1 and 2 connect to the carrier's same 3.3 V rail. Do not apply 5 V. Carrier header SM15B-GHS-TB(LF)(SN) mates to GHR-15V-S with SSHL-002T-P0.2 contacts (26-30 AWG, 0.76-1.0 mm insulation). SSH-003T-P0.2 is not the specified compatible contact. Confirm the numbered connector orientation on both ends before powering; a cable is not assumed straight-through by color.

ST7796S write cycle minimum 66 ns gives a 15.15 MHz ceiling. Set SPI writes to 12 MHz (83.3 ns) and reads at most 6 MHz (150 ns minimum read cycle). Start bring-up at 1-5 MHz. One RGB565 full frame is 307200 bytes; ideal transmission takes 204.8 ms at 12 MHz, or 4.88 frames/s before protocol overhead. For 30 Hz UI scheduling, use small partial updates, typically 10-15% of the screen. No 30 Hz full-screen claim is made. Budget display current at 200 mA despite the maker FAQ's approximately 63 mA operating example.

NXP LCD-PAR-S035 was rejected because detailed panel/mating information was not publicly obtainable. BuyDisplay ER-TFT035IPS-6-4405 remained unqualified after datasheet access failure. Their pin assignments are not used in this revision.

Mechanical concept: landscape display spans board coordinates x=33.78..126.22, y=17..78 in a separate front plane. It overhangs the carrier's top by 13 mm, leaving room above the lower-right keys. The enclosure must accommodate that extension, display depth, microphone opening and antenna connector. This is an allocation drawing, not a completed enclosure or a verified clearance stack.
