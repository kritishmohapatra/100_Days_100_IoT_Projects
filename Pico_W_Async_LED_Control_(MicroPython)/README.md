
# 🌐 Pico 2 W Async LED Control (MicroPython)

An **asynchronous web-based LED control project** using **Raspberry Pi Pico 2 W**, **MicroPython**, and **uasyncio**.  
Control the onboard LED from any browser using a simple web interface.

This project demonstrates async networking, non-blocking WiFi connection, and lightweight IoT-style device control.

---

## 🚀 Features

- ✅ Raspberry Pi Pico 2W WiFi control
- ✅ Async web server using `uasyncio`
- ✅ Browser-based LED ON/OFF control
- ✅ Non-blocking WiFi connection
- ✅ Clean HTML + Fetch API interface
- ✅ Lightweight and fast
- ✅ Perfect starter async IoT template

---

## 🧰 Requirements

- Raspberry Pi Pico 2 W
- MicroPython firmware installed
- Thonny / rshell / mpremote
- WiFi network
- USB cable

---

## 📦 Libraries Used

- `uasyncio`
- `network`
- `machine.Pin`

(All included in MicroPython Pico W firmware)

---


### 2️⃣ Upload Code

Save the script as:
 main.py


Upload to Pico 2 W using Thonny or mpremote.

---

### 3️⃣ Configure WiFi

Edit inside code:

```python
SSID = "your_wifi_name"
PASSWORD = "your_wifi_password"
```
## ▶️ Run Device

Run `main.py` — serial console will show:
```
Connecting WiFi...
IP: xxx.xxx.xxx.xxx
Server running on port 80
```
---


## 🌍 How to Use

1. Connect Pico2W to power  
2. Check printed IP address in serial console  
3. Open your web browser  
4. Enter: http://DEVICE_IP

Example:

http://192.168.1.45


5. Web page will open  
6. Click buttons:

- **ON → LED turns ON**
- **OFF → LED turns OFF**

---

## 🧠 How It Works

- Pico 2W connects to WiFi asynchronously
- Async server listens on port 80
- Browser sends `/on` or `/off` requests
- LED state changes instantly
- No blocking loops are used

---

## 🖥️ Web Interface

- Simple HTML control page
- Fetch API used for sending commands
- Status updates shown instantly
- No page reload required

---


## 🔬 Use Cases

- IoT device control
- Async networking learning
- MicroPython web server template
- Home automation starter
- Embedded async programming practice

---

## 🚀 Future Upgrades (Optional Ideas)

- LED status auto refresh
- Toggle button control
- Sensor data display
- Dashboard UI
- MQTT integration
- ThingsBoard support

## 🧑‍💻 Author

**Kritish Mohapatra**  
B.Tech Electrical Engineering (3rd Year)  
IoT | Embedded Systems | MicroPython | ESP32  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!

Happy hacking 🚀
