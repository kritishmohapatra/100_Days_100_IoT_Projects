# Smart Home Automation
### ESP32 + DHT22 + 4 Relay + Adafruit IO + MicroPython

> Cloud-connected smart home system  control 4 appliances from anywhere via Adafruit IO dashboard or mobile app. Simulated on Wokwi.

---

## Features

- Real-time temperature & humidity monitoring via DHT22
- Control 4 relays independently from Adafruit IO dashboard
- Manual control via dashboard toggles or mobile app
- Auto-reconnect on WiFi/MQTT drop
- Wokwi simulation ready

---

## Tech Stack

| Component | Role |
|---|---|
| ESP32 DevKit v1 | Main microcontroller |
| DHT22 | Temperature & humidity sensor |
| 4x Relay Module | Controls AC appliances |
| Adafruit IO | MQTT cloud dashboard |
| MicroPython | Firmware |
| Wokwi | Online simulation |

---

## Circuit Diagram

| Pin | Connected To | Purpose |
|---|---|---|
| GPIO 4 | DHT22 DATA | Sensor data |
| GPIO 26 | Relay 1 IN | Fan |
| GPIO 27 | Relay 2 IN | Humidifier |
| GPIO 25 | Relay 3 IN | Light |
| GPIO 33 | Relay 4 IN | Spare |
| 3V3 | DHT22 VCC | Sensor power |
| 5V | All Relay VCC | Relay power |
| GND | All GND | Common ground |

---

## Adafruit IO Setup

### 1. Create these 6 Feeds

```
temperature
humidity
relay1-control
relay2-control
relay3-control
relay4-control
```

### 2. Create Dashboard — add these blocks

| Block | Feed | Settings |
|---|---|---|
| Gauge | temperature | - |
| Gauge | humidity | - |
| Toggle | relay1-control | ON=1, OFF=0 |
| Toggle | relay2-control | ON=1, OFF=0 |
| Toggle | relay3-control | ON=1, OFF=0 |
| Toggle | relay4-control | ON=1, OFF=0 |

---

## Relay Mapping

| Relay | Pin | Appliance |
|---|---|---|
| Relay 1 | GPIO 26 | Fan |
| Relay 2 | GPIO 27 | Humidifier |
| Relay 3 | GPIO 25 | Light |
| Relay 4 | GPIO 33 | Spare |

> All relays are manually controlled via Adafruit IO dashboard toggles.

---

## How to Run

**Step 1 — Adafruit IO**
1. Create free account at [io.adafruit.com](https://io.adafruit.com)
2. Create 6 feeds listed above
3. Create dashboard and add blocks
4. Copy AIO Username + Key from the yellow key icon

**Step 2 — Wokwi**
1. Go to [wokwi.com](https://wokwi.com) → New Project → ESP32 + MicroPython
2. Paste `main.py` in the editor
3. Paste `diagram.json` in the diagram tab
4. Fill in `AIO_USERNAME` and `AIO_KEY`
5. Press Play

**Step 3 Mobile**
1. Install **Adafruit IO** app (Play Store / App Store)
2. Login with same account
3. Open Smart Home dashboard
4. Toggle relays from anywhere

---

## Expected Serial Output

```
Hardware initialized
Connecting to Wokwi-GUEST...
WiFi connected: 10.0.0.2
Subscribed: your_username/feeds/relay1-control
Subscribed: your_username/feeds/relay2-control
Subscribed: your_username/feeds/relay3-control
Subscribed: your_username/feeds/relay4-control
Starting main loop...
Temp: 27.5C  Hum: 55.0%  Relays: [0, 0, 0, 0]
MQTT IN [.../relay1-control] -> 1
Relay 1 (Fan) ON
```

---

## Adafruit IO Free Plan Limits

| Limit | Value |
|---|---|
| Requests/minute | 30 |
| Max feeds | 10 |
| Max dashboards | 5 |
| Data retention | 30 days |

> This project uses ~6 requests/minute — well within free plan limits.

---

## Security Note

> Never commit your AIO Key to GitHub. Use environment variables or a separate `secrets.py` file and add it to `.gitignore`.

```python
# secrets.py  (add this to .gitignore)
AIO_USERNAME = "your_username"
AIO_KEY      = "aio_your_key"
```

```
# .gitignore
secrets.py
```

---



## Simulate on Wokwi

[![Open in Wokwi](https://img.shields.io/badge/Open%20in-Wokwi-green?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMiAxNWwtNS01IDEuNDEtMS40MUwxMCAxNC4xN2w3LjU5LTcuNTlMMTkgOGwtOSA5eiIvPjwvc3ZnPg==)](https://wokwi.com/projects/466515572360075265)

---

*Built with MicroPython on ESP32 | Part of 100 Days 100 IoT Projects*
##  Author

**Kritish Mohapatra**  
B.Tech Electrical Engineering (3rd Year)  
IoT | Embedded Systems | MicroPython | ESP32  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!

Happy hacking 🚀

