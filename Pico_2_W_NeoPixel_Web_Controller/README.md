
# NeoPixel 8-Ring Web Controller
### Raspberry Pi Pico 2W + MicroPython

Control a WS2812B NeoPixel 8-ring via a browser-based web interface hosted on the Pico 2W itself — no app, no cloud, no extra hardware.

---

##  Hardware Required

| Component | Quantity |
|---|---|
| Raspberry Pi Pico 2W | 1 |
| WS2812B NeoPixel 8-Ring | 1 |
| 330Ω Resistor (optional) | 1 |
| Jumper Wires | 3 |
| Breadboard | 1 |

---

##  Wiring
![circuit_image](Circuit_Diagram/circuit_image.png)

| NeoPixel Ring | Pico 2W |
|---|---|
| VCC | VBUS — Pin 40 (5V) |
| GND | GND — Pin 38 |
| DIN | GP0 — Pin 1 |

>  Use **VBUS (5V)** for VCC, not the 3.3V pin — colors will be off on 3.3V power.  
> A 330Ω resistor on the DIN line is optional but recommended for signal protection.

---


##  Getting Started

### 1. Flash MicroPython on Pico 2W
Download the latest MicroPython `.uf2` from [micropython.org](https://micropython.org/download/RPI_PICO2_W/) and flash it.

### 2. Edit WiFi Credentials
Open `main.py` and update:
```python
SSID     = "YourWiFiName"
PASSWORD = "YourPassword"
```

>  Pico 2W supports **2.4GHz WiFi only** — 5GHz networks will not connect.

### 3. Upload to Pico
Use [Thonny IDE](https://thonny.org/) to upload `main.py` and run it.

### 4. Open the Web Interface
Check the Serial monitor for the IP address:
```
IP: 192.168.x.x
URL: http://192.168.x.x
```
Open that URL in your browser (phone or PC on the **same WiFi network**).

---

##  Features

| Feature | Description |
|---|---|
| **Solid** | Fill all pixels with selected color |
| **Rainbow** | Smooth rotating rainbow cycle |
| **Breathe** | Selected color fades in and out |
| **Turn Off** | All pixels off |
| **Color Picker** | Choose any color from the palette |
| **Brightness Slider** | Adjust brightness from 1% to 100% |

---

##  Web UI Preview

- Dark-themed mobile-friendly interface
- Color picker for full RGB control
- Brightness slider with live update
- One-tap animation buttons

---

##  How It Works

1. Pico 2W connects to WiFi and starts a lightweight HTTP server on port 80
2. Browser sends `GET /set?mode=rainbow` style requests on button tap
3. Pico parses the request, updates mode/color/brightness globals
4. Animation loop runs non-blocking using `setblocking(False)` on the socket
5. `gc.collect()` runs every 100 frames to keep RAM clean

---

##  API Endpoints

| Endpoint | Example | Action |
|---|---|---|
| `/` | `http://ip/` | Serves the HTML web UI |
| `/set?mode=` | `/set?mode=rainbow` | Change animation mode |
| `/set?color=` | `/set?color=%23ff0000` | Change color (hex) |
| `/set?brightness=` | `/set?brightness=50` | Set brightness (1–100) |

---

##  Dependencies

- `neopixel` — built-in to MicroPython, no install needed
- `network`, `socket`, `math`, `gc` — all built-in

---



##  Troubleshooting

| Problem | Fix |
|---|---|
| Only blue pixels lighting up | Move VCC to VBUS (5V), not 3.3V pin |
| Nothing lighting up | Check GND connection — most common cause |
| IP not showing in Serial | Wrong SSID/Password or 5GHz network |
| Web page not loading | Phone and Pico must be on same WiFi |
| Page loads but buttons don't work | Disable mobile data, use WiFi only |

---

##  Author

**Kritish Mohapatra**

B.Tech Electrical Engineering (3rd Year)

IoT | Embedded Systems | MicroPython | ESP32

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!