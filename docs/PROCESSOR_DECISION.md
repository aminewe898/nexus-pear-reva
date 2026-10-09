# Picking the brain — no hype tax

| Platform | Relevant fit | Decision |
|---|---|---|
| ESP32-S3 + PSRAM | Wi-Fi/BLE, native USB, I2S and SPI; external-antenna module available | Selected for remote inference and modest partial-screen UI |
| ESP32-P4 + radio companion | More graphics throughput; extra processor/radio and power complexity | Better if full-screen animation becomes essential |
| STM32H743 + radio | Strong real-time/audio resources; separate network hardware | More integration cost for this network-first interface |
| RP2350 + radio | Flexible PIO; separate Wi-Fi and additional UI integration | No clear advantage for this feature set |
| Small Linux SBC | Rich application stack and graphics | More boot, storage, power and enclosure overhead |

This decision depends on the SPI display's roughly 4.88 ideal full frames/s at 12 MHz. It supports low-motion interfaces and partial updates. A requirement for continuous 30/60 full frames/s requires a different display bus or platform. No current complete assembled-system quotes were obtained for the alternatives.
