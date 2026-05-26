
# Adafruit IO MQTT LED Control — Raspberry Pi Pico 2W

Control the onboard LED of a Raspberry Pi Pico 2W remotely over MQTT using Adafruit IO. Send ON/OFF commands from the Adafruit IO dashboard, a mobile app, or any MQTT client, and the Pico responds in real time.

---

## How It Works

The Pico 2W connects to your WiFi network, then establishes a persistent MQTT connection to `io.adafruit.com`. It subscribes to a feed called `led-control`. Whenever a message arrives on that feed:

- `ON` turns the onboard LED on
- `OFF` turns it off

The main loop calls `check_msg()` every 100ms in a non-blocking manner, so the board stays responsive. On any connection error, it automatically reconnects.

---

## Hardware Required

- Raspberry Pi Pico 2W
- USB cable (for power / flashing)

No external components needed — uses the onboard LED.

---

## Dependencies

- MicroPython firmware for Pico 2W (v1.23 or later recommended)
- `umqttsimple.py` — lightweight MQTT client for MicroPython
  - Source: https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.simple
- `secrets.py` — your credentials file (see below)

---



## Setup

### 1. Adafruit IO Feed

- Log in at https://io.adafruit.com
- Go to Feeds and create a new feed named `led-control`
- Note your username and active key from the AIO Key button on the dashboard

### 2. secrets.py

Create a `secrets.py` file on the Pico with the following structure:

```python
secrets = {
    "ssid"     : "your_wifi_ssid",
    "password" : "your_wifi_password",
    "aio_user" : "your_adafruit_io_username",
    "aio_key"  : "your_adafruit_io_key"
}
```

### 3. Flash Files

Copy these files to the Pico using Thonny or mpremote:

```
main.py
umqttsimple.py
secrets.py
```

### 4. Run

Power the board or press Run in Thonny. Open the serial monitor to see connection status.

```
Connecting to WiFi...
WiFi connected: 192.168.x.x
Subscribed to: your_username/feeds/led-control
```

---

## Controlling the LED

From the Adafruit IO dashboard, add a Toggle block linked to `led-control` with ON/OFF values.

You can also publish manually via any MQTT client:

```
Broker   : io.adafruit.com
Port     : 1883
Username : your_aio_username
Password : your_aio_key
Topic    : your_aio_username/feeds/led-control
Payload  : ON  or  OFF
```

---

## Serial Output

```
Received: ON
LED ON
Received: OFF
LED OFF
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| WiFi not connecting | Double-check SSID and password in secrets.py |
| MQTT auth error | Verify aio_user and aio_key; check for extra spaces |
| LED not responding | Confirm feed name is exactly `led-control` |
| umqttsimple not found | Copy umqttsimple.py to the root of the Pico filesystem |

---



##  Author

**Kritish Mohapatra**  
B.Tech Electrical Engineering (3rd Year)  
IoT | Embedded Systems | MicroPython | ESP32  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!

Happy hacking 🚀

