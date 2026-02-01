

# 🔌 Flask Server Based LED Control using MicroPython (ESP32 / Pico W)

This project demonstrates a **clean client–server IoT architecture** where a **Flask server controls an LED** connected to an **ESP32 or Raspberry Pi Pico W** running **MicroPython**.

The Flask server acts as the **central controller**, while the microcontroller works as a **client** that periodically fetches the LED state and updates the hardware accordingly.

---

## 🚀 Project Overview

- Flask provides a **web dashboard** with ON/OFF buttons
- LED state is stored on the Flask server
- ESP32 / Pico W polls the server for LED status
- LED turns ON/OFF based on server command
- Frontend uses **HTML + JavaScript (fetch API)**

---

## 🧠 Architecture

    Browser (HTML + JS)
    ↓
    Flask Server (API + UI)
    ↑
    ESP32 / Pico W (MicroPython Client)
    ↓
    LED / Relay


✔ Single server (Flask)  
✔ ESP acts only as client  
✔ No raw socket handling  
✔ Clean & scalable design  

---

## 📁 Project Structure

    main/
    │
    ├── app.py
    ├── templates/
    │ └── index.html
    │
    ├── static/
    │ └── script.js
    │
    └── main.py (MicroPython code for ESP32 / Pico W)


---

## ⚙️ Requirements

### 🖥️ Flask Server
- Python 3.x
- Flask

```bash
pip install flask
```

## 🔧 Hardware

 - ESP32 or Raspberry Pi Pico W

- Onboard LED or external LED + resistor

- WiFi connection

## 🧪 Flask Server Code (app.py)

- Hosts the web dashboard

- Stores LED state

- Provides REST API for ESP
---
## Available Routes'
| Endpoint     | Method | Description          |
| ------------ | ------ | -------------------- |
| `/`          | GET    | Web UI               |
| `/led/on`    | GET    | Turn LED ON          |
| `/led/off`   | GET    | Turn LED OFF         |
| `/led/state` | GET    | Get LED state (JSON) |


## 🌐 Frontend (HTML + JS)

- HTML served from `templates/index.html`
- JavaScript served from `static/script.js`
- Uses `fetch()` API (no page reload)
- Live LED status display on the dashboard

---

## 🤖 MicroPython Client (`main.py`)

- Connects to WiFi
- Polls Flask server every **1 second**
- Reads LED state from `/led/state`
- Updates GPIO accordingly

### Compatible Boards
- ESP32
- Raspberry Pi Pico W

---

## ▶️ How to Run

### 1️⃣ Start Flask Server
```bash
python app.py
```
Open in browser:
```
http://<FLASK_IP>:5000
```

### 2️⃣ Flash MicroPython Code
- Upload main.py to ESP32 / Pico W

- Update Flask server IP in code:
```
SERVER = "http://<FLASK_IP>:5000/led/state"
```
- Reset the board

### 3️⃣ Control LED 🎉
- Click LED ON / OFF buttons in browser

- LED changes state in real time on the device

## ✅ Features
- Clean client–server architecture
- No page reload UI (fetch-based)
- Real-time LED status monitoring
- Flask best practices (templates/, static/)
- Beginner-friendly and interview-ready design

## 🔮 Future Improvements
- Relay / AC appliance control
- Multiple LEDs or devices
- Authentication token
- Database integration (SQLite)
- MQTT integration
- Sensor + control dashboard

---
## ❤️Author
**Kritish Mohapatra**  
B.Tech Electrical Engineering (3rd Year)  
IoT | Embedded Systems | MicroPython | ESP32  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!

Happy hacking 🚀
