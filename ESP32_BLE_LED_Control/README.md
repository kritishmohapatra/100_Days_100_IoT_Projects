# ESP32 BLE LED Control 
> MicroPython + Bluetooth Low Energy

---

##  Project Overview

This project demonstrates controlling the onboard LED of an ESP32 via Bluetooth Low Energy (BLE) using MicroPython. Any BLE UART-compatible smartphone app (such as nRF Connect) can be used to send commands and toggle the LED wirelessly.

---

##  Features

-  **BLE UART Communication** — Uses the Nordic UART Service (NUS)
-  **LED Control** — Toggle LED via `LED_ON` / `LED_OFF` commands
-  **Status Query** — Query the current LED state with the `STATUS` command
-  **Connection Indicator** — LED blinks when disconnected, solid ON when connected

---

##  Hardware Requirements

| Component        | Details              |
|-----------------|----------------------|
| Microcontroller | ESP32 DevKit v1      |
| Onboard LED Pin | GPIO 2               |
| LED Type        | Standard LED         |
| BLE Support     |  Built-in          |
| MicroPython     | v1.19+               |

---

##  Software Requirements

- MicroPython firmware flashed on the ESP32
- [Thonny IDE](https://thonny.org) — for uploading code to the board
- [nRF Connect](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp) app (Android/iOS)
- `ubluetooth` module (built into MicroPython)

---



##  BLE Commands

| Command    | Action           | Board Response           |
|-----------|------------------|--------------------------|
| `LED_ON`  | Turn the LED ON  | `LED is ON`              |
| `LED_OFF` | Turn the LED OFF | `LED is OFF`             |
| `STATUS`  | Query LED state  | `LED is ON / LED is OFF` |

---

##  LED Behavior

| LED State    | Meaning                        |
|-------------|--------------------------------|
|  Blinking  | BLE Disconnected (advertising) |
|  Solid ON  | BLE Connected                  |
|  OFF       | `LED_OFF` command received     |

---

##  How to Use

1. **Flash MicroPython** onto your ESP32 — [micropython.org](https://micropython.org/download/esp32/)
2. **Upload the code** using Thonny IDE and click Run
3. **Open nRF Connect** app on your smartphone
4. **Scan for devices** — look for `ESP32`
5. **Connect** and navigate to the TX Characteristic
6. **Enable Notifications** on the TX Characteristic (tap the bell icon)
7. **Write `LED_ON`** to the RX Characteristic and send

---

##  BLE Service UUIDs (Nordic UART Service)

| Service / Characteristic   | UUID                                    |
|---------------------------|-----------------------------------------|
| Nordic UART Service (NUS)  | `6E400001-B5A3-F393-E0A9-E50E24DCCA9E` |
| RX Characteristic (Write)  | `6E400002-B5A3-F393-E0A9-E50E24DCCA9E` |
| TX Characteristic (Notify) | `6E400003-B5A3-F393-E0A9-E50E24DCCA9E` |

---

##  Troubleshooting

| Problem                         | Solution                                                 |
|--------------------------------|----------------------------------------------------------|
| `OSError: -128` on send         | Enable Notifications on TX Characteristic in nRF Connect |
| LED not responding to commands  | Check that GPIO 2 is the correct LED pin on your board   |
| Device not visible during scan  | Restart the board and scan again                         |
| BLE not working at all          | Ensure MicroPython v1.19+ with `ubluetooth` support      |

---

##  Author

**Kritish Mohapatra**

B.Tech Electrical Engineering — 3rd Year

IoT | Embedded Systems | MicroPython | ESP32

OUTR, Bhubaneswar

---

## ⭐ Support

If you found this project helpful, give it a ⭐ on GitHub and feel free to fork it!

Happy Hacking! 🚀