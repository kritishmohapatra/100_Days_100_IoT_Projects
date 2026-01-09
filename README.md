# 100 Days 100 IoT Projects 🚀

Welcome to my **100 Days 100 IoT Projects** repository!  
This repo showcases my journey of learning and implementing **IoT & Embedded Systems projects** using **ESP32, Raspberry Pi Pico**, and **MicroPython**.  

Each project is designed to teach a specific concept, sensor, or IoT technique — from basic analog/digital readings to web-based dashboards.

---
![100 Days 100 IoT Projects Banner](IMAGES/banner.png)



## 🧰 Technologies & Boards Used

- **Microcontrollers:** ESP32, Raspberry Pi Pico  
- **Programming:** MicroPython  
- **Sensors & Modules:** LDR, Potentiometer, DHT11, HC-SR04, 7-Segment Display, and more  
- **Concepts Covered:** ADC, PWM, Digital I/O, Web Server, GPIO Control, Sensor Interfacing  

---

## 📂 Project List
| Day | Project | Board / Sensor | Description |
|-----|----------|----------------|-------------|
| 1 | [Auto Night Light](Auto_Night_Light_using_LDR_(ESP32_+_MicroPython)/README.md) | ESP32 + LDR | Automatic LED turns ON/OFF based on ambient light |
| 2 | [Dimmer LED using Potentiometer](Dimmer_LED_using_Potentiometer_(MicroPython)/README.md) | ESP32 + Potentiometer | LED brightness controlled via potentiometer using ADC + PWM |
| 3 | [DHT11 Temperature & Humidity Web Server](DHT11_Web_Server_using_ESP32_&_MicroPython/README.md) | ESP32 + DHT11 | Reads temperature & humidity and displays on a live web page |
| 4 | [1-Digit Seven Segment Display](Single_Digit_Seven_Segment_Display_with_Raspberry_Pi-Pico_(MicroPython)/README.md) | Raspberry Pi Pico + 7-Segment | Displays numeric output using GPIO control |
| 5 | [Mini Weather Station (DHT11 + LCD)](DHT11_LCD_Display_using_ESP8266_&_MicroPython/README.md) | ESP8266 + DHT11 + I²C LCD | Displays real-time temperature & humidity on 16x2 LCD without flickering |
| 6 | [RGB Color Mixer using Potentiometers](RGB_Color_Mixer_using_Potentiometers_(ESP32_+_MicroPython)/README.md) | ESP32 + 3 Potentiometers + RGB LED | Mix RGB colors by adjusting potentiometers using ADC and PWM |
| 7 | [Potentiometer Bar Graph Display](Potentiometer_Visualizer/README.md) | ESP32 + Potentiometer + 10 LEDs | Visualize analog input as a 10-LED bar graph using ADC mapping |
| 8 | [MQ4 Gas Leak Detection System](MQ4_Gas_Leak_Detection_System_using_ESP32_and_MicroPython/README.md) | ESP32 + MQ4 Sensor + Buzzer | Detects methane gas concentration using MQ4 sensor and triggers alert when gas level exceeds threshold |
| 9 | [Basic RTC Clock (Serial Monitor Display)](Basic_RTC_Clock_(_Serial_Monitor_Display_)/README.md) | ESP8266 + DS3231 RTC | Displays real-time date, time, and temperature on Serial Monitor using DS3231 RTC |
| 10 | [IoT Button Counter using ESP8266 & MicroPython](IoT_Button_Counter_using_ESP8266_&_MicroPython/README.md) | ESP8266 + 3 Push Buttons | Counts button presses (Increment, Decrement, Reset) and displays live counter on webpage |
| 11 | [MicroPython-Based 8×8 LED Matrix Animation Display using ESP8266](MicroPython_Based_8×8_LED_Matrix_Animation_Display_using_ESP8266/README.md) | ESP8266 + MAX7219 8×8 LED Matrix | Displays custom animations (heart beat) on 8×8 LED matrix using MicroPython |
| 12 | [PIR Motion Detector using Raspberry Pi Pico 2W & MicroPython](PIR_Motion_Detector_using_Raspberry_Pi_Pico_2W_&_MicroPython/README.md) | Raspberry Pi Pico 2W + PIR Sensor | Detects motion using PIR sensor and indicates using built-in LED with MicroPython |
| 13 | [Bluetooth-Based Wireless LED Control System](Bluetooth_Based_Wireless_LED_Control_System/README.md) | Raspberry Pi Pico 2W + HC-05 | Wireless LED ON/OFF control using MicroPython + HC-05 Bluetooth module |
| 14 | [Pico W Web Servo Controller](Pico_W_Web_Servo_Controller/README.md) | Raspberry Pi Pico 2W + Servo Motor | Control servo angle (0–180°) from browser via WiFi |
| 15 | [ClimaPixel — Mini Weather Display](ClimaPixel_Mini_Weather_Display/README.md) | ESP32/ESP8266 + DHT11 + SSD1306 OLED | Real-time temperature & humidity display with icons on OLED using MicroPython |
| 16 | [TM1637 Button-Press Counter using ESP8266 & MicroPython](ESP8266_TM1637_Button_Press_Counter_(MicroPython)/README.md) | ESP8266 + TM1637 + Push Button | Counts button presses and displays live counter on TM1637 4-digit display |
| 17 | [IoT Relay Control Web Server (Raspberry Pi Pico 2W)](IoT_Relay_Control_Web_Server_(Raspberry_Pi_Pico_2W)/README.md) | Raspberry Pi Pico 2W + Relay Module | Web-based relay control using MicroPython with a smooth slide switch UI and real-time ON/OFF status over WiFi |
| 18 | [Blynk-Based IoT Relay Control (Raspberry Pi Pico 2 W)](Blynk_Based_IoT_Relay_Control_(MicroPython)/README.md) | Raspberry Pi Pico 2 W + Relay Module | Mobile app–based relay control using Blynk IoT and MicroPython with real-time ON/OFF control over Wi-Fi |
| 19 | [NTP Digital Clock using TM1637 & ESP8266 (MicroPython)](ESP8266_NTP_Digital_Clock_MicroPython/README.md) | ESP8266 + TM1637 | Internet-synchronized digital clock using NTP with accurate HH:MM display, blinking colon, and custom segment mapping in MicroPython |
| 20 | [Smart IR Object Detection System](Smart_IR_Object_Detection_System/README.md) | ESP8266 + IR Sensor + LED + Buzzer | Detects the presence of an object using an IR sensor and triggers LED and buzzer alerts in real time using MicroPython |
| 21 | [ESP32 Password Lock System](Password_Lock_System_using_ESP32/README.md) | ESP32 + Keypad + LCD + LEDs | Implements a secure password authentication system using a keypad and LCD with visual LED feedback, developed in MicroPython |
| 22 | [Blynk Controlled DC Brushless Fan](Blynk_Controlled_DC_Brushless_Fan/README.md) | Raspberry Pi Pico W + Relay + DC Brushless Fan | Controls a DC brushless fan remotely using the Blynk IoT platform and a relay module, implemented in MicroPython |
| 23 | [ESP32 Hotspot Setup](ESP32_Hotspot_(Access_Point)_Setup_MicroPython/README.md) | ESP32 | Configures ESP32 in Access Point (Hotspot) mode using MicroPython, enabling direct device-to-device connectivity without internet |
| 24 | [Voice-Controlled LED System](Voice_Activated_LED_Control_System/README.md) | Arduino + Python | Controls an LED using voice commands processed in Python and sent to Arduino via serial communication |
| 25 | [Arduino RGB LED Control with Python GUI](Interactive_LED_Control_System/README.md) | Arduino + Python | Controls an RGB LED using a Python GUI built with CustomTkinter and PyFirmata2, allowing color selection, individual LED on/off control, and brightness adjustment via sliders |
| 26 | [Clap Toggle Switch using ESP32 (MicroPython)](Clap_Toggle_Switch_using_ESP32_&_Digital_Sound_Sensor_(MicroPython)/README.md) | ESP32 + MicroPython | A clap-controlled toggle switch using a digital sound sensor where one clap turns the output ON and the next clap turns it OFF, implemented with debounce logic for reliable operation |
| 27 | [IR Sensor Telegram Alert using ESP32 (MicroPython)](ESP32_IR_Sensor_Telegram_Alert_(MicroPython)/README.md) | ESP32 + MicroPython | An IR sensor–based object detection system that sends real-time alert notifications to a Telegram channel whenever motion or object presence is detected near the sensor |



---
## 🌟 Features

- Step-by-step learning from **basic to advanced IoT concepts**  
- Hands-on experience with **analog & digital sensors**  
- Integration of **web interfaces** for IoT visualization  
- Ready-to-use **MicroPython code** for each project  
- Clean **folder-wise organization** for easy navigation  

---

## 📈 Roadmap

- Complete **100 IoT projects** in 100 days  
- Each project will have a **dedicated folder, main.py, README.md, and circuit diagram**  
- Upcoming projects include: Ultrasonic Sensors, Gas Sensors, Relay Control, OLED Displays, RGB LEDs, Smart Home Automation, and more  

---

## 🧑‍💻 Author

**Kritish Mohapatra**  
Third Year B.Tech, Electrical Engineering  
📡 Focused on IoT, Embedded Systems, and MicroPython Projects  

---

⭐ If you like this repository, give it a **star** on GitHub and follow for more IoT projects!
