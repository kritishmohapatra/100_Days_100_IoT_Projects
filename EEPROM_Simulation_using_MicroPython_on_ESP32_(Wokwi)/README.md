
#  EEPROM Simulation using MicroPython on ESP32 (Wokwi)

This project demonstrates how to simulate EEPROM behavior on an ESP32 using **MicroPython** and the internal file system in Wokwi. Since ESP32 does not have true EEPROM, we emulate it using a binary file and implement byte-level read/write operations similar to Arduino EEPROM.

---
##  Wokwi Simulation

[![Open in Wokwi](https://img.shields.io/badge/Wokwi-Simulate%20Project-blue?logo=espressif&logoColor=white)](https://wokwi.com/projects/454569980045734913)

Click the badge above to run the live ESP32 MicroPython EEPROM simulation in Wokwi.


##  Features

-  EEPROM simulation using file storage  
-  Byte-level read and write functions  
-  String storage with null termination  
-  Write-only-if-changed logic (reduces flash wear)  
-  Persistent data across resets in Wokwi  
-  Arduino EEPROM-style string handling  

---

##  Concept

ESP32 does not contain real EEPROM. In this project:

- A binary file (`eeprom.dat`) acts as EEPROM memory  
- File index = EEPROM address  
- Each stored value = one byte  
- `0x00` is used as string terminator  
- File → EEPROM
- Index → Address
- Byte → Stored Data


---

##  Technology Used

- ESP32  
- MicroPython  
- Wokwi Simulator  
- File-based persistent storage  

---

##  Memory Configuration

```python
EEPROM_FILE = "eeprom.dat"
EEPROM_SIZE = 512
```
##  Functions Implemented

### EEPROM Core Functions

- **eeprom_init()** → Creates EEPROM file if not present  
- **eeprom_read_byte(addr)** → Reads one byte from address  
- **eeprom_write_byte(addr, val)** → Writes one byte to address  

---

### String Functions

**save_string(address, text)**

- Writes string byte-by-byte  
- Writes only if value changed  
- Adds null terminator  

**read_string(address)**

- Reads bytes until null byte found  
- Converts bytes back to string  

---

##  How to Run (Wokwi)

1. Open Wokwi  
2. Create new **ESP32 MicroPython** project  
3. Paste code into `main.py`  
4. Click **Run**  
5. Enter string in serial console  
6. Restart simulation to verify persistence  

---

##  Example Output
```
Enter a string to save in EEPROM:
hello
String saved in EEPROM.
Stored Text in EEPROM: hello


Second run with same value:



Enter a string to save in EEPROM:
hello
String is same as previous one.
Stored Text in EEPROM: hello

```
---

##  Applications

- Device configuration storage  
- WiFi credential saving  
- User preferences  
- IoT node settings  
- Calibration values  

---

##  Notes

- Data persists across simulation restarts (unless storage is reset)  
- Max string length depends on `EEPROM_SIZE`  
- Designed for learning and simulation purposes  

---

##  Future Improvements

- Store integers and floats  
- JSON config storage  
- Encrypted EEPROM data  
- Wear leveling logic  
- OLED display integration  
----
##  Author

**Kritish Mohapatra**  
B.Tech Electrical Engineering (3rd Year)  
IoT | Embedded Systems | MicroPython | ESP32  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!

Happy hacking 🚀