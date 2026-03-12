
#  micropidash: Lightweight MicroPython IoT Dashboard

**micropidash** is a high-performance, asynchronous web dashboard library specifically designed for microcontrollers like the **Raspberry Pi Pico 2W** (RP2350/RP2040) and ESP32. It enables the creation of real-time, responsive web interfaces for IoT projects using minimal MicroPython code.


**Full project**: https://github.com/kritishmohapatra/micropidash

**Author:** [Kritish Mohapatra]  


---

##  Key Features
* **Asynchronous Engine:** Built on `uasyncio` for non-blocking, multi-tasking performance.
* **Real-Time Sync:** AJAX-based polling ensures all connected devices (Mobile & Laptop) stay synced without page refreshes.
* **Client-Side Theming:** Every connected user can independently toggle between Dark and Light modes.
* **Order Preservation:** Uses alphabetical sorting for widget IDs to ensure your layout stays exactly as intended.
* **Memory Efficient:** Optimized for devices with limited RAM, featuring chunked data transmission and frequent garbage collection.

---

##  Installation

1. Upload `micropidash.py` to your microcontroller's root directory.
2. Create a `main.py` file to implement your project logic.
3. Ensure your device is connected to a stable 2.4GHz Wi-Fi network.

---
##  Project Structure
    ├── micropidash/
    │ ├── init.py
    │ └── micropidash.py 
    │
    ├── examples/
    |  ├── basic_1.py
    │  └── esp_32_example.py 
    │
    ├── README.md
    └── LICENSE
##  API Documentation

### `Dashboard(title)`
Creates a new dashboard instance with the specified title.
* **title**: (String) The name displayed at the top of your web dashboard.

---

### `add_toggle(id, label)`
Adds a binary switch (On/Off) to the dashboard.
* **id**: (String) Unique identifier for the widget. Also used for alphabetical sorting on the UI.
* **label**: (String) The text displayed above the switch.

---

### `add_label(id, label)`
Adds a text box designed for displaying live sensor data or status strings.
* **id**: (String) Unique identifier for the widget.
* **label**: (String) The descriptive text for the data being shown.

---

### `add_level(id, label, color)`
Adds a graphical progress bar, perfect for humidity, tank levels, or battery percentage.
* **id**: (String) Unique identifier for the widget.
* **label**: (String) The descriptive text for the progress bar.
* **color**: (Hex/CSS Color) The color of the fill bar (e.g., `#2196F3` or `red`).
* **Value Range**: Expects an integer between 0 and 100.

---

### `update_value(id, value)`
Injects new data into an existing widget. This change is pushed instantly to all connected web clients via the next poll.
* **id**: (String) The ID of the widget you want to update.
* **value**: (String/Int) The new data to display.

---
##  Quick Start (Simple Example)

Use this minimal example to test your connection and ensure the dashboard is being served correctly on your local network.

```python
from micropidash import Dashboard
import network 

# 1. WiFi Setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect('YOUR_SSID', 'YOUR_PASSWORD')

print("Connecting...")
while not wlan.isconnected(): pass
print("Connected! IP:", wlan.ifconfig()[0])

# 2. Dashboard Initialization
dash = Dashboard("MicroPiDash v1.0")

# 3. Adding Basic Widgets
dash.add_toggle("led", "Test Switch")      # A binary toggle
dash.add_label("status", "System Status")  # A text display
dash.add_level("level", "Signal Strength") # A progress bar (0-100)

# 4. Start the Web Server
# Access the dashboard via the IP address printed above
dash.run()
```
![Dashboard UI](dashboard_images/img_1.png)
![Dashboard UI](dashboard_images/img_3.jpeg)

###  ESP32 Onboard LED Example


```python
import machine, network, uasyncio as asyncio
from micropidash import Dashboard

# 1. ESP32 Pin Setup (Most boards use GPIO 2 for built-in LED)
led = machine.Pin(2, machine.Pin.OUT)

# 2. WiFi Connectivity
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('YOUR_SSID', 'YOUR_PASSWORD')

print("Connecting...")
while not wlan.isconnected(): pass
print("Server Live at IP:", wlan.ifconfig()[0])

# 3. Dashboard Configuration
dash = Dashboard("ESP32 Control Hub")
dash.add_toggle("1_led", "Built-in LED")
dash.add_label("2_status", "Live Status")

# 4. Hardware & Web UI Sync Task
async def sync_task():
    while True:
        # Dashboard UI state ko physical LED se link karna
        led.value(dash.elements["1_led"]["value"])
        
        # Dashboard par status update bhejni
        state = "GLOWING" if led.value() else "OFF"
        dash.update_value("2_status", f"LED is {state}")
        
        await asyncio.sleep(0.5)

# 5. Execution
async def main():
    asyncio.create_task(sync_task())
    dash.run()

asyncio.run(main())
```
###  Rpi pico 2w Example
``` python
import machine, network, uasyncio as asyncio
import dht
from micropidash import Dashboard

# 1. Pin Setup
led = machine.Pin('LED', machine.Pin.OUT)
sensor = dht.DHT11(machine.Pin(28))  # GP28

# 2. WiFi Connectivity
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('YOUR_SSID', 'YOUR_PASSWORD')  
print("Connecting...")
while not wlan.isconnected(): pass
print("Server Live at IP:", wlan.ifconfig()[0])

# 3. Dashboard Configuration
dash = Dashboard("Pico Control Hub")
dash.add_toggle("1_led", "Built-in LED")
dash.add_label("2_status", "LED Status")
dash.add_label("3_temp", "Temperature (°C)")
dash.add_label("4_humidity", "Humidity (%)")
dash.add_level("5_hum_bar", "Humidity Level", "#2196F3")

# 4. Sync Task
async def sync_task():
    while True:
        # LED control
        led.value(dash.elements["1_led"]["value"])
        state = "GLOWING" if led.value() else "OFF"
        dash.update_value("2_status", f"LED is {state}")

        # DHT11 reading
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            dash.update_value("3_temp", f"{temp} °C")
            dash.update_value("4_humidity", f"{hum} %")
            dash.update_value("5_hum_bar", hum)
        except Exception as e:
            print("Sensor error:", e)

        await asyncio.sleep(2)  # DHT11 needs ~2s between readings

# 5. Execution
async def main():
    asyncio.create_task(sync_task())
    dash.run()

asyncio.run(main())
```
![Dashboard UI](dashboard_images/img_2.png)
![Dashboard UI](dashboard_images/img_4.jpeg)
##  Contributing
As an **Electrical Engineering student**, I built **micropidash** to simplify MicroPython IoT development and bridge the gap between hardware and web interfaces. 

If you find bugs, have feature ideas, or want to optimize the code further, feel free to open an **issue** or submit a **pull request**! Let's build the future of embedded systems together.

---
##  Author

**Kritish Mohapatra**  
->[GitHub](https://github.com/kritishmohapatra)  
-> kritishmohapatra06norisk@gmail.com  

 *Made with passion for Embedded Systems and MicroPython learners.*