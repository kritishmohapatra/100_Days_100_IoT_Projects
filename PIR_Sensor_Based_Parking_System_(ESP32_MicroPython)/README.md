
# PIR Sensor Based Parking System (ESP32 + MicroPython)

A simple smart parking slot monitoring system built using PIR motion sensors and an ESP32. Slot occupancy status is shown live on an SSD1306 OLED display.
## Simulate on Wokwi

[![Open in Wokwi](https://img.shields.io/badge/Open%20in-Wokwi-green?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMiAxNWwtNS01IDEuNDEtMS40MUwxMCAxNC4xN2w3LjU5LTcuNTlMMTkgOGwtOSA5eiIvPjwvc3ZnPg==)](https://wokwi.com/projects/467086691355950081)
## Overview

This project tracks the occupancy of 2 parking slots using PIR motion sensors. Since PIR sensors detect motion rather than static presence, each slot's state is tracked using a toggle approach: the first motion event (a car entering the slot) marks it as FULL, and the next motion event (the car leaving) marks it as FREE again.

## Hardware Required

- ESP32 development board
- 2x PIR motion sensor module (e.g. HC-SR501)
- SSD1306 OLED display, 128x64, I2C
- Breadboard and jumper wires

## Wiring

| Component         | ESP32 Pin |
|-------------------|-----------|
| PIR Sensor 1 OUT  | GPIO 32   |
| PIR Sensor 2 OUT  | GPIO 33   |
| PIR Sensors VCC   | 5V        |
| PIR Sensors GND   | GND       |
| OLED SDA          | GPIO 21   |
| OLED SCL          | GPIO 22   |
| OLED VCC          | 3.3V      |
| OLED GND          | GND       |

## How It Works

1. Each PIR sensor is read continuously for a rising edge (LOW to HIGH transition), which marks a fresh motion event.
2. On a valid motion event, the corresponding slot's occupied state is toggled (FREE becomes FULL, FULL becomes FREE).
3. A 3 second cooldown after each toggle prevents the same motion event from triggering multiple toggles.
4. The OLED display updates only when a slot's state actually changes, showing each slot's status and the total number of free slots.

## Software Requirements

- MicroPython firmware flashed on the ESP32
- `ssd1306.py` driver uploaded to the board alongside the main script

## Usage

1. Flash MicroPython firmware onto the ESP32.
2. Upload `ssd1306.py` and the main script (`main.py`) to the board.
3. Power on the circuit and allow 30 to 60 seconds for the PIR sensors to warm up before relying on readings.
4. Trigger a PIR sensor (e.g. by walking in front of it) to toggle that slot between FREE and FULL on the display.


## Limitations

PIR sensors detect motion, not continuous presence, so this toggle-based approach can be triggered by unrelated motion near a slot (such as someone walking past). For more reliable occupancy detection, an ultrasonic distance sensor or an IR break-beam pair would be a better long-term choice.

## Future Improvements

- Replace PIR sensors with ultrasonic or IR break-beam sensors for continuous, reliable occupancy detection
- Add MQTT integration to push slot status to a remote dashboard
- Add a buzzer or LED indicator per slot for quick visual status at a glance



##  Author

**Kritish Mohapatra**  
B.Tech Electrical Engineering (3rd Year)  
IoT | Embedded Systems | MicroPython | ESP32  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!

Happy hacking 🚀

