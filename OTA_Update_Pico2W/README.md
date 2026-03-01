# OTA Update using Raspberry Pi Pico 2 W & GitHub

A WiFi-based OTA (Over-the-Air) update system that automatically downloads and applies new code from GitHub without physically connecting the device to a computer, using MicroPython on Raspberry Pi Pico 2 W.

This project demonstrates WiFi connectivity, HTTP requests, file management, and automatic firmware updates on Raspberry Pi Pico 2 W.

---

## Features

- Automatic code update over WiFi on every boot
- Fetches latest version from GitHub (raw.githubusercontent.com)
- Version comparison to avoid unnecessary updates
- Auto-restart after successful update
- Serial monitor logging for update status
- Works fully offline if no update is available

---

## How It Works

```
Pico boots up
    ↓
Connects to WiFi
    ↓
Checks version.txt on GitHub
    ↓
If new version found → downloads main.py → restarts
If already latest   → runs normally
```

---

## Hardware Required

- Raspberry Pi Pico 2 W
- USB cable
- WiFi connection

---

## Software Requirements

- MicroPython firmware for Raspberry Pi Pico 2 W
- Thonny IDE
- GitHub account (public repository)

---

## File Structure

| File | Location | Purpose |
|------|----------|---------|
| `boot.py` | Pico | Runs automatically on every startup, triggers OTA check |
| `ota.py` | Pico | Handles WiFi connection and GitHub update logic |
| `main.py` | GitHub + Pico | Your actual application code |
| `version.txt` | GitHub | Stores the current version number |
| `local_version.txt` | Pico | Stores the last installed version |

---

## Installation

1. Flash MicroPython firmware to Raspberry Pi Pico 2 W
2. Upload `ota.py` to the Pico using Thonny
3. Upload `boot.py` to the Pico using Thonny
4. Update WiFi credentials and GitHub details in `ota.py`
5. Add `main.py` and `version.txt` to your GitHub repo
6. Run — Pico will auto-update on every boot!

---

## How to Push an Update

1. Edit `main.py` on GitHub with your new code
2. Change `version.txt` to the next version (e.g. `1.0.0` → `1.0.1`)
3. Commit the changes
4. Reboot Pico — it will detect and apply the update automatically!

---

## Code Overview

- Connects to WiFi using `network` module
- Fetches `version.txt` from GitHub using `urequests`
- Compares remote version with locally saved version
- If different — downloads new `main.py` and saves it to Pico
- Updates `local_version.txt` and restarts using `machine.reset()`

---

## Serial Monitor Output

```
Connecting to WiFi...
WiFi connected! IP: 192.168.1.x
Local version:  1.0.0
Remote version: 1.0.1
New update found! Downloading...
Update done! Restarting...
```

---

## Notes

- `boot.py` runs before `main.py` on every Pico startup — perfect for OTA checks.
- Internet connection is required for OTA updates; Pico runs existing code if offline.
- Only `main.py` is updated via OTA; `ota.py` and `boot.py` stay on the Pico.
- GitHub's raw URL is used for direct file access without any API authentication.

---

## Future Improvements

- OTA update for multiple files at once
- Rollback to previous version on failed update
- OLED display showing update status
- Telegram bot notification on successful update
- Scheduled OTA check every N minutes
- Web dashboard to trigger updates remotely

---

## Author
**Kritish Mohapatra**

B.Tech Electrical Engineering (3rd Year)
IoT | Embedded Systems | MicroPython | Raspberry Pi Pico

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!

Happy hacking 🚀