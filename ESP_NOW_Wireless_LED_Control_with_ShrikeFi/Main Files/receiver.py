import network
import espnow
from machine import Pin, SoftI2C
import ssd1306

i2c = SoftI2C(scl=Pin(6), sda=Pin(7))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

led1 = Pin(4, Pin.OUT)
led2 = Pin(5, Pin.OUT)

led1_state = False
led2_state = False

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()
e.active(True)

def update_oled(msg):
    oled.fill(0)
    oled.text("ShrikeFi", 0, 0)
    oled.text(msg, 0, 20)
    oled.show()

update_oled("Waiting...")

while True:
    host, msg = e.recv()
    if msg:
        if msg == b'BTN1':
            led1_state = not led1_state
            led1.value(led1_state)
            update_oled("LED1 ON" if led1_state else "LED1 OFF")
        elif msg == b'BTN2':
            led2_state = not led2_state
            led2.value(led2_state)
            update_oled("LED2 ON" if led2_state else "LED2 OFF")
