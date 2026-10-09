# Pin lore — the actual wiring

These tables are generated from the checked native design. Nets are engineering identifiers; NC pins are omitted. Shared peripheral 3.3 V removes independently powered display/microphone/SD domains. Do not externally power any harness.

## U1 — ESP32-S3-WROOM-1U-N16R8

| Pin | Signal | Net |
|---|---|---|
| 1 | GND | GND |
| 2 | 3V3 | +3V3 |
| 3 | EN | EN |
| 4 | IO4 | LCD_MOSI |
| 6 | IO6 | LCD_CS |
| 7 | IO7 | LCD_BL |
| 8 | IO15 | I2C_SCL |
| 9 | IO16 | I2C_SDA |
| 10 | IO17 | I2S_BCLK_SRC |
| 11 | IO18 | I2S_WS_SRC |
| 12 | IO8 | TP_RST |
| 13 | USB_D- | USB_DM |
| 14 | USB_D+ | USB_DP |
| 17 | IO9 | TP_INT |
| 18 | IO10 | LCD_MISO |
| 20 | IO12 | LCD_SCLK_SRC |
| 21 | IO13 | LCD_DC_SRC |
| 22 | IO14 | LCD_RST |
| 23 | IO21 | I2S_TX_SRC |
| 24 | IO47 | MIC_DATA |
| 25 | IO48 | STATUS |
| 27 | IO0 | BOOT |
| 31 | IO38 | PERIPH_EN |
| 32 | IO39 | SD_SCK_SRC |
| 33 | IO40 | SD_MOSI_SRC |
| 34 | IO41 | SD_MISO |
| 35 | IO42 | SD_CS |
| 36 | RXD0 | UART_RX |
| 37 | TXD0 | UART_TX |
| 39 | IO1 | KEY_ADC |
| 40 | GND | GND |
| 41 | GND | GND |

## J1 — USB-C 5V / USB2 FS

| Pin | Signal | Net |
|---|---|---|
| A1 | GND | GND |
| A4 | VBUS | VBUS |
| A5 | CC1 | CC1 |
| A6 | D+ | USB_DP_CONN |
| A7 | D- | USB_DM_CONN |
| A9 | VBUS | VBUS |
| A12 | GND | GND |
| B1 | GND | GND |
| B4 | VBUS | VBUS |
| B5 | CC2 | CC2 |
| B6 | D+ | USB_DP_CONN |
| B7 | D- | USB_DM_CONN |
| B9 | VBUS | VBUS |
| B12 | GND | GND |
| SH | SHIELD | GND |

## J2 — WAVESHARE 29318 GH15

| Pin | Signal | Net |
|---|---|---|
| 1 | +3V3 | +3V3 |
| 2 | +3V3 | +3V3 |
| 3 | GND | GND |
| 4 | LCD_MISO | LCD_MISO |
| 5 | LCD_MOSI | LCD_MOSI |
| 6 | LCD_SCLK | LCD_SCLK |
| 7 | DISPLAY_SD_CS | DISPLAY_SD_CS |
| 8 | LCD_CS | LCD_CS |
| 9 | LCD_DC | LCD_DC |
| 10 | LCD_RST | LCD_RST |
| 11 | LCD_BL | LCD_BL |
| 12 | I2C_SDA | I2C_SDA |
| 13 | I2C_SCL | I2C_SCL |
| 14 | TP_INT | TP_INT |
| 15 | TP_RST | TP_RST |
| MP | MOUNT | GND |

## J3 — LEFT AMP HARNESS

| Pin | Signal | Net |
|---|---|---|
| 1 | +5V_AUDIO | +5V |
| 2 | GND | GND |
| 3 | AMP_LEFT_SD | AMP_LEFT_SD |
| 5 | I2S_TX | AMP_TX |
| 6 | I2S_BCLK | AMP_BCLK |
| 7 | I2S_WS | AMP_WS |

## J4 — RIGHT AMP HARNESS

| Pin | Signal | Net |
|---|---|---|
| 1 | +5V_AUDIO | +5V |
| 2 | GND | GND |
| 3 | AMP_RIGHT_SD | AMP_RIGHT_SD |
| 5 | I2S_TX | AMP_TX |
| 6 | I2S_BCLK | AMP_BCLK |
| 7 | I2S_WS | AMP_WS |

## J5 — MIC HARNESS

| Pin | Signal | Net |
|---|---|---|
| 1 | +3V3 | +3V3 |
| 2 | GND | GND |
| 3 | I2S_BCLK | MIC_BCLK |
| 4 | MIC_DATA | MIC_DATA |
| 5 | I2S_WS | MIC_WS |
| 6 | GND | GND |

## J6 — 3V3 SD HARNESS

| Pin | Signal | Net |
|---|---|---|
| 1 | +3V3 | +3V3 |
| 2 | GND | GND |
| 3 | SD_SCK | SD_SCK |
| 4 | SD_MOSI | SD_MOSI |
| 5 | SD_MISO | SD_MISO |
| 6 | SD_CS | SD_CS |

## J7 — UART RECOVERY

| Pin | Signal | Net |
|---|---|---|
| 1 | GND | GND |
| 2 | UART_TX | UART_TX |
| 3 | UART_RX | UART_RX |
| 4 | EN | EN |
| 5 | BOOT | BOOT |
| 6 | +3V3 | +3V3 |

## J8 — I2C EXPANSION

| Pin | Signal | Net |
|---|---|---|
| 1 | +3V3 | +3V3 |
| 2 | GND | GND |
| 3 | I2C_SCL | I2C_SCL |
| 4 | I2C_SDA | I2C_SDA |

Boot/reset retain ESP32 defaults. IO35/36/37 are reserved by octal PSRAM and unused. IO3/45/46 straps are unused. GPIO38 only enables translated audio signals. GPIO1 reads a one-key-at-a-time ADC ladder; calibration and released-key saturation handling are firmware requirements.
