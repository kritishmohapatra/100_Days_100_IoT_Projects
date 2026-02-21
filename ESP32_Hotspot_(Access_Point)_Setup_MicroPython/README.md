
#  ESP32 Hotspot (Access Point) Setup – MicroPython

##  Project Overview
This project demonstrates how to configure an **ESP32 as a Wi-Fi Hotspot (Access Point)** using **MicroPython**.  
Users can directly connect to the ESP32 using a mobile phone or laptop **without internet**, forming the base for local IoT dashboards and configuration portals.

---

##  Features
- ESP32 works in **Access Point (AP) mode**
- No external Wi-Fi or internet required
- Secure hotspot using WPA/WPA2
- Displays ESP32 local IP address
- Foundation for:
  - Local Web Server
  - Device Configuration Portal
  - Smart Home & IoT Systems

---

##  Hardware Requirements
- ESP32 Development Board  
- USB Cable  
- Laptop / PC  
- Mobile phone or laptop (for testing)

---

##  Software Requirements
- MicroPython firmware for ESP32  
- Thonny / uPyCraft / any MicroPython IDE  
- USB driver (CP2102 / CH340 if required)

---

##  How It Works
- ESP32 is set to **AP (Access Point) mode**
- Creates its own Wi-Fi network (SSID)
- Other devices connect directly to ESP32
- ESP32 assigns a local IP (usually `192.168.4.1`)

---

##  How to Run
1. Flash MicroPython firmware on the ESP32  
2. Upload `main.py` to the ESP32 using Thonny / uPyCraft  
3. Open the Serial Monitor  
4. On your mobile or laptop, open Wi-Fi settings and connect to:
   - **SSID:** ESP32_HOTSPOT  
   - **Password:** 12345678  

##  Output
- ESP32 Hotspot appears in the available Wi-Fi list  
- Device connects successfully without internet  
- Serial Monitor displays:
- Hotspot status
- ESP32 local IP address (usually `192.168.4.1`)

---

##  Notes
- Wi-Fi password must be **at least 8 characters**
- Default ESP32 Access Point IP is `192.168.4.1`
- Restart the ESP32 if the hotspot does not appear
- AP mode works offline (no internet required)

---

##  Future Enhancements
- Add a web server on ESP32
- Create an HTML-based control dashboard
- Build a Wi-Fi configuration portal
- Integrate sensors and real-time data display
- Use as a base for Smart Home or IoT systems

---


##  Author

**Kritish Mohapatra**  
MicroPython | ESP32 | Embedded Systems | IoT Projects  
GitHub: [https://github.com/kritishmohapatra]