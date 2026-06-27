import network
import espnow
from machine import Pin
import time

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()
e.active(True)

RECEIVER_MAC = b''
e.add_peer(RECEIVER_MAC)

btn1 = Pin(12, Pin.IN, Pin.PULL_UP)
btn2 = Pin(13, Pin.IN, Pin.PULL_UP)

btn1_prev = 1
btn2_prev = 1
btn1_time = 0
btn2_time = 0
DEBOUNCE_MS = 50

while True:
    now = time.ticks_ms()
    b1 = btn1.value()
    b2 = btn2.value()

    if b1 != btn1_prev and time.ticks_diff(now, btn1_time) > DEBOUNCE_MS:
        if b1 == 0:
            e.send(RECEIVER_MAC, b'BTN1')
        btn1_prev = b1
        btn1_time = now

    if b2 != btn2_prev and time.ticks_diff(now, btn2_time) > DEBOUNCE_MS:
        if b2 == 0:
            e.send(RECEIVER_MAC, b'BTN2')
        btn2_prev = b2
        btn2_time = now

    time.sleep_ms(10)
