import network, time
from machine import Pin
from umqttsimple import MQTTClient
from secrets import secrets

# ── Hardware ──────────────────────────────────
led = Pin("LED", Pin.OUT)

# ── WiFi connect ──────────────────────────────
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets["ssid"], secrets["password"])
while not wlan.isconnected():
    time.sleep(0.5)
    print("Connecting to WiFi...")
print("WiFi connected:", wlan.ifconfig()[0])

# ── MQTT config ───────────────────────────────
AIO_USER  = secrets["aio_user"]
AIO_KEY   = secrets["aio_key"]
BROKER    = "io.adafruit.com"
FEED      = f"{AIO_USER}/feeds/led-control"
CLIENT_ID = "pico2w-led"

def on_message(topic, msg):
    val = msg.decode().strip()
    print("Received:", val)
    if val == "ON":
        led.value(1)
        print("LED ON")
    elif val == "OFF":
        led.value(0)
        print("LED OFF")


client = MQTTClient(
    client_id = CLIENT_ID,
    server    = BROKER,
    port      = 1883,
    user      = AIO_USER,
    password  = AIO_KEY,
    keepalive = 60
)
client.set_callback(on_message)
client.connect()
client.subscribe(FEED)
print(f"Subscribed to: {FEED}")

while True:
    try:
        client.check_msg()   
        time.sleep(0.1)
    except Exception as e:
        print("Error, reconnecting...", e)
        time.sleep(2)
        client.connect()
        client.subscribe(FEED)
