# NTP Synchronized Clock ESP32 + I2C LCD

A real-time clock built with **MicroPython** on ESP32 that syncs time over WiFi using NTP and displays it on a 16×2 I2C LCD.

---

##  Demo

```
13:45:22  Sat
13/06/2026
```

---

##  Hardware Required

| Component | Quantity |
|-----------|----------|
| ESP32 Dev Board | 1 |
| 16×2 LCD with I2C backpack (PCF8574) | 1 |
| Jumper Wires | 4 |

---

##  Wiring

| LCD Pin | ESP32 Pin |
|---------|-----------|
| SDA | GPIO 21 |
| SCL | GPIO 22 |
| VCC | 3.3V / 5V |
| GND | GND |

---

##  Dependencies

Download and flash these two files onto your ESP32 alongside `main.py`:

- [`lcd_api.py`]()
- [`i2c_lcd.py`]()

---

##  Configuration

Edit these lines in `main.py`:

```python
SSID = "YourWiFiName"
PASSWORD = "YourPassword"
TZ_OFFSET = 5*3600 + 30*60   # IST (UTC +5:30) — change for your timezone
```

> **I2C Address:** Default is `0x27`. If LCD doesn't show anything, try `0x3F`.

---

##  How It Works

1. ESP32 connects to WiFi
2. `ntptime.settime()` syncs the RTC with NTP server (UTC)
3. `TZ_OFFSET` converts UTC → local time (IST)
4. LCD updates every second:
   - **Row 1:** `HH:MM:SS  Day`
   - **Row 2:** `DD/MM/YYYY`

---

##  Tested On

- MicroPython v1.28.0 — Generic ESP32
- [Wokwi Simulator](https://wokwi.com/projects/466649758369128449) (use `"Wokwi-GUEST"` as SSID)

---

##  Author

**Kritish Mohapatra**  
B.Tech Electrical Engineering (3rd Year)  
IoT | Embedded Systems | MicroPython | ESP32  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!

Happy hacking 🚀

