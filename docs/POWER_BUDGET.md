# Watt could go wrong? — power budget

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
