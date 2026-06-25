import network
import time
from umqttsimple import MQTTClient  # Fixed the import here
from neopixel import NeoPixel
from machine import Pin
import json

# NeoPixel setup
NUM_PIXELS = 8
PIN = 15
np = NeoPixel(Pin(PIN), NUM_PIXELS)

# WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Wokwi-GUEST", "")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nWiFi connected:", wlan.ifconfig()[0])

# MQTT callback
def on_message(topic, msg):
    print(f"Received message on topic {topic}: {msg}")
    try:
        # JSON parse karna
        data = json.loads(msg)
        r = data.get('r', 0)
        g = data.get('g', 0)
        b = data.get('b', 0)
        
        # Saare pixels ka color set karna
        for i in range(NUM_PIXELS):
            np[i] = (r, g, b)
        np.write()
        print(f"NeoPixel updated to RGB: ({r}, {g}, {b})")
    except Exception as e:
        print("Error parsing JSON:", e)

# Main
connect_wifi()

client = MQTTClient("esp32-neo", "your ip", port=1883)
client.set_callback(on_message)
client.connect()
client.subscribe(b"neopixel/color")
print("MQTT connected & Subscribed to neopixel/color!")

while True:
    client.check_msg()
    time.sleep(0.1)