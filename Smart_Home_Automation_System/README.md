# Smart Home Automation System with Blynk, ESP8266 and DHT11

This project implements a home automation system using an ESP8266 microcontroller, a DHT11 temperature and humidity sensor, and the Blynk IoT platform. It allows users to remotely control four LED Bulbs and monitor temperature via the Blynk app.

## Prerequisites

* **ESP8266 Development Board:** (e.g., NodeMCU)
* **DHT11 Temperature and Humidity Sensor**
* **LED Bulbs (4)**
* **220 Ohm Resistors (4):** For current limiting with the LEDs.
* **MicroPython Firmware:** Flashed onto the ESP8266.
* **Blynk Account and App:** Set up on your smartphone.
* **Wi-Fi Network:** With internet access.
* **USB Cable:** For connecting the ESP8266 to your computer.

## Hardware Setup

1.  **LED Connections:**
    * Connect the anode (longer leg) of each LED to the following ESP8266 pins:
        * LED BULB 1: D0 (GPIO16)
        * LED BULB 2: D1 (GPIO5)
        * LED BULB 3: D2 (GPIO4)
        * LED BULB 4: D3 (GPIO0)
    * Connect the cathode (shorter leg) of each LED to ground (GND) through a 220 Ohm resistor(For LEDs).

2.  **DHT11 Connection:**
    * Connect the VCC pin of the DHT11 to 3.3V on the ESP8266.
    * Connect the GND pin of the DHT11 to GND on the ESP8266.
    * Connect the data pin of the DHT11 to D5 (GPIO14) on the ESP8266.

3.  **ESP8266 Connection:**
    * Connect the ESP8266 to your computer using a USB cable for power and uploading code.

## Circuit Diagram
![ESP8266 Home Automation System with Blynk and DHT11](Circuit_Diagram/circuit_image_(1).png)


## Software Setup

1.  **Flash MicroPython Firmware:**
    * Download the latest MicroPython firmware for ESP8266.
    * Use a tool like `esptool.py` to flash the firmware onto your ESP8266.

2.  **Install Required Libraries:**
    * Use `mip` or `upip` to install the `network`, `machine`, `BlynkLib`, and `dht` libraries on your ESP8266.

3.  **Blynk App Setup:**
    * Create a Blynk account and project.
    * Add four buttons to control the LEDs, linked to virtual pins V1, V2, V3, and V4.
    * Add a gauge widget to display the temperature, linked to virtual pin V5.
    * Obtain the Blynk authorization token for your project.

4.  **Configure Wi-Fi and Blynk Token:**
    * Replace `wifissid`, `wifipass`, and `auth` in the Python code with your Wi-Fi credentials and Blynk authorization token.

5.  **Upload the Code:**
    * Use a tool like `ampy` or Thonny to upload the Python code to your ESP8266.

## Code Explanation

* **`network`:** For Wi-Fi connectivity.
* **`machine`:** For controlling GPIO pins.
* **`BlynkLib`:** For communication with the Blynk app.
* **`time`:** For delays.
* **`dht`:** For reading data from the DHT11 sensor.
* **Wi-Fi Connection:** Connects the ESP8266 to your Wi-Fi network.
* **Blynk Initialization:** Establishes a connection with the Blynk server.
* **LED Control:** Controls the LEDs based on button presses in the Blynk app.
* **DHT11 Reading:** Reads temperature data from the DHT11 sensor.
* **Blynk Virtual Writes:** Sends LED status and temperature data to the Blynk app.
* **Error Handling:** Includes `try...except` blocks to handle potential errors during value conversion.
* **Main Loop:** Continuously runs the Blynk processes and reads sensor data.

## How to Use

1.  **Power On:** Power on the ESP8266.

2.  **Connect to Blynk:** The ESP8266 will connect to your Wi-Fi and Blynk.

3.  **Control LEDs:** Use the buttons in the Blynk app to turn the LED BULBs on or off.

4.  **Monitor Temperature:** The temperature will be displayed on the gauge widget in the Blynk app.

## Important Notes

* **Wi-Fi Credentials:** Ensure your Wi-Fi credentials are correct.
* **Blynk Token:** Ensure your Blynk authorization token is correct.
* **Pin Assignments:** Double-check the pin assignments in the code and hardware setup.
* **MicroPython Libraries:** Make sure the required MicroPython libraries are installed.
* **Error Handling:** The code includes basic error handling, but you can add more robust error checking.
## Practical Video

<video controls src="Circuit_Diagram/Practical.mp4" title="circuit_image_(1).png"></video>
https://github.com/user-attachments/assets/bef6c9de-e6a4-403e-8396-ddf06b5a8266

## 🛠 Customization

* Add more sensors and actuators.
* Implement more complex automation logic.
* Use different Blynk widgets for a richer user interface.
* Add a web interface for local control.
* Utilize other cloud IoT platforms.

## Future Improvements

* Implement humidity monitoring and display.
* Add logging and data storage.
* Integrate with other smart home devices.
* Improve error handling and robustness.

## Author
**Kritish Mohapatra**  
B.Tech Electrical Engineering (3rd Year)  
IoT | Embedded Systems | MicroPython | ESP32  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!

Happy hacking 🚀
