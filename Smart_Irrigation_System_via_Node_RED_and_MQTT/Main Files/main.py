import network
import time
from umqttsimple import MQTTClient
from machine import Pin, ADC
import dht
import json

# Pin setup
DHT_PIN = 15
RED_LED = Pin(4, Pin.OUT)
GREEN_LED = Pin(5, Pin.OUT)

sensor = dht.DHT22(Pin(DHT_PIN))
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

# Starting state
RED_LED.value(0)
GREEN_LED.value(1)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Wokwi-GUEST", "")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nWiFi connected:", wlan.ifconfig()[0])

def on_message(topic, msg):
    message = msg.decode()
    print("Command received:", message)
    if message == "PUMP_ON":
        RED_LED.value(1)
        GREEN_LED.value(0)
        print("ALERT: Pump ON")
    elif message == "PUMP_OFF":
        RED_LED.value(0)
        GREEN_LED.value(1)
        print("SAFE: Pump OFF")

def read_moisture():
    raw = pot.read()
    moisture = int((4095 - raw) / (4095 - 1250) * 100)
    return max(0, min(100, moisture))

connect_wifi()

client = MQTTClient("esp32-irrigation", "ip", port=1883)
client.set_callback(on_message)
client.connect()
client.subscribe(b"esp32/pump_command")
print("MQTT connected!")

while True:
    client.check_msg()
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        moisture = read_moisture()

        payload = json.dumps({
            "temperature": temp,
            "humidity": hum,
            "moisture": moisture
        })

        client.publish(b"esp32/sensor_data", payload)
        print("Published:", payload)

    except Exception as e:
        print("Sensor error:", e)

    time.sleep(1)