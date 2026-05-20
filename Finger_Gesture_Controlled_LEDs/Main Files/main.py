from machine import Pin
import sys
import time

leds = {
    "LED1": Pin(2, Pin.OUT),
    "LED2": Pin(5, Pin.OUT),
    "LED3": Pin(6, Pin.OUT),
    "LED4": Pin(7, Pin.OUT),
    "LED5": Pin(8, Pin.OUT),
}

for led in leds.values():
    led.value(0)

print("ESP READY")

while True:
    cmd = sys.stdin.readline()
    if not cmd:
        continue
    cmd = cmd.strip().upper()
    if ":" in cmd:
        name, action = cmd.split(":", 1)
        if name in leds:
            if action == "ON":
                leds[name].value(1)
            elif action == "OFF":
                leds[name].value(0)
    time.sleep(0.05)
