# The vibe check needs a multimeter — bring-up plan

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
