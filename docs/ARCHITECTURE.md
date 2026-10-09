# The pear has range — architecture

NEXUS PEAR is a USB-powered desktop interface to a remote AI service. ESP32-S3-WROOM-1U-N16R8 provides Wi-Fi, Bluetooth, native USB, 16 MB flash and 8 MB PSRAM. The enclosure concept is a pear; the display is a normal rectangle. No battery, charger, local language-model inference or USB host is included.

USB-C VBUS passes a 3 A/24 V PTC, TVS and TPS25940L protected switch. An always-on LDO supplies TUSB320LAI and hardware logic. Only a source advertising 3 A on CC enables the main supply. AP63203 generates shared 3.3 V for the processor, display, microphone and microSD. The two audio modules use protected 5 V; TXU0104 translates and isolates their I2S signals. GPIO38 enables audio data, with a hardware pull-down.

The Waveshare 29318 module provides ST7796S SPI IPS graphics and FT6336U two-point capacitive touch. A digital I2S microphone mounts at the top acoustic opening. Two MAX98357A modules drive separate 8-ohm Visaton speakers at the lower sides. Six physical lower-right keys share an ADC ladder. A real external Taoglas RP-SMA antenna connects to the module U.FL socket through CAB.774.

Carrier: 100 x 90 mm, four layers. F.Cu and B.Cu carry most signals; In1.Cu is ground, In2.Cu is 3.3 V with isolated raw-power/CC routing. Full functionality still needs firmware, harness assembly, enclosure and bench qualification. DO NOT ORDER is the release status.
