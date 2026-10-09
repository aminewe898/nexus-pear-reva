# Let the pear cook — audio and microphone

Two Adafruit 3006 MAX98357A mono modules create stereo outputs. BCLK/WS/data are shared after TXU0104 translates 3.3 V logic to protected 5 V. The translator has power-off isolation/Ioff; its OE defaults low through 100 kOhm. Output damping resistors are 33 ohm; amplifier data inputs have 100 kOhm pull-downs. GPIO38 enables audio only after supply checks.

Breakout channel selection includes its internal 1 MOhm pull-up and IC 100 kOhm pull-down: SD to 5 V through 82 kOhm selects left (approximately 2.85 V), 560 kOhm selects right (approximately 1.09 V). GAIN floats for nominal 9 dB. Verify these levels on the purchased module revision. Speakers: Visaton K28.40, MPN 2945, 8 ohm, 2 W rated. Class-D bridge terminals must never connect to ground or a grounded oscilloscope clip.

The simultaneous-load design allowance caps acoustic output at 0.75 W per channel. Unrestricted full scale can exceed the power budget. Firmware must implement a calibrated limit; that implementation and calibration are not delivered or tested here.

Adafruit 3421 SPH0645LM4H uses 3.3 V and separate 33-ohm-damped 3.3 V microphone BCLK/WS. It does not receive 5 V translator outputs. Target shared I2S clock: 48 kHz x 64 bits = 3.072 MHz. Capture the appropriate signed slot and resample to 16 kHz for upload if required. Begin with half-duplex push-to-talk. Echo cancellation, voice quality and acoustic isolation remain implementation/bench work. Place the bottom-port microphone at a top enclosure acoustic opening with a sealed path; do not block its port.
