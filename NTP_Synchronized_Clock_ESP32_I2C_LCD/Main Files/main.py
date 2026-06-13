from machine import Pin, I2C
from i2c_lcd import I2cLcd
import time, network, ntptime

# ========== WIFI ==========
SSID = "Wokwi-GUEST"
PASSWORD = ""

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
print("Connecting WiFi...")
while not wlan.isconnected():
    time.sleep(1)
print("WiFi Connected!")

# ========== NTP ==========
ntptime.settime()

# ========== LCD I2C ==========
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

TZ_OFFSET = 5*3600 + 30*60
DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
def pad(s, n=16):
    return s + " " * (n - len(s))
# ========== MAIN LOOP ==========
while True:
    t = time.time() + TZ_OFFSET
    tm = time.localtime(t)

    line1 = "{:02d}:{:02d}:{:02d}  {}".format(tm[3], tm[4], tm[5], DAYS[tm[6]])
    line2 = "{:02d}/{:02d}/{:04d}".format(tm[2], tm[1], tm[0])

    lcd.move_to(0, 0)
    lcd.putstr(pad(line1))
    lcd.move_to(0, 1)
    lcd.putstr(pad(line2))

    time.sleep(1)