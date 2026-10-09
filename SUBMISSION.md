# NEXUS PEAR REV A — pear pressure

A small desktop device with a normal rectangular touch screen, stereo speakers, a top microphone, Wi-Fi, a real external antenna and six buttons. The pear has range. The antenna is doing an actual job.

This submission includes an editable eleven-sheet KiCad design, a routed four-layer 100 x 90 mm carrier, BOM/RFQ, manufacturing exports, PDFs, a board render and engineering calculations. Remote services perform model inference; the ESP32-S3 handles interface, networking and audio.

The revision replaces the display with a publicly documented module, adds hardware 3 A USB source qualification and protected power, addresses power-off signal injection, corrects manufacturer land patterns/order codes, and improves critical routing. Final ERC and DRC results are included with the actual native files.

**Engineering review candidate — DO NOT ORDER.** Physical startup/fault/thermal/audio/USB tests, fabricator impedance approval, complete live quotes and remaining mechanical/footprint tolerance checks are still required. Firmware and a tested prototype are not part of this submission. Read docs/DESIGN_REVIEW_REVA.md for the precise completion status. The connectivity vibe check passed; release needs measurements.
