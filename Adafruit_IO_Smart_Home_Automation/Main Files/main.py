# ============================================================
#  Smart Home - ESP32 + DHT22 + 4 Relay + Adafruit IO
#  MicroPython | Wokwi Simulation
# ============================================================

import time
import dht
import machine
import network
import ubinascii
from umqttsimple import MQTTClient

# -- CREDENTIALS ---------------------------------------------
AIO_USERNAME  = ""   # change this
AIO_KEY       = ""        # change this
WIFI_SSID     = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# -- FEEDS ---------------------------------------------------
TEMP_FEED   = f"{AIO_USERNAME}/feeds/temperature"
HUM_FEED    = f"{AIO_USERNAME}/feeds/humidity"
RELAY_FEEDS = [
    f"{AIO_USERNAME}/feeds/relay1-control",
    f"{AIO_USERNAME}/feeds/relay2-control",
    f"{AIO_USERNAME}/feeds/relay3-control",
    f"{AIO_USERNAME}/feeds/relay4-control",
]

# -- PINS ----------------------------------------------------
DHT_PIN      = 4
RELAY_PINS   = [26, 27, 25, 33]
RELAY_LABELS = ["Fan", "Humidifier", "Light", "Spare"]

# -- INIT HARDWARE -------------------------------------------
sensor = dht.DHT22(machine.Pin(DHT_PIN))
relays = [machine.Pin(p, machine.Pin.OUT) for p in RELAY_PINS]
for r in relays:
    r.value(0)
print("Hardware initialized")

# -- WIFI ----------------------------------------------------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to " + WIFI_SSID + "...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")
    if wlan.isconnected():
        print("\nWiFi connected: " + wlan.ifconfig()[0])
        return True
    print("\nWiFi failed!")
    return False

# -- MQTT CALLBACK (Cloud -> Relay) --------------------------
def on_message(topic, msg):
    topic = topic.decode()
    msg   = msg.decode().strip().lower()
    print("MQTT IN [" + topic + "] -> " + msg)

    for i, feed in enumerate(RELAY_FEEDS):
        if feed in topic:
            if msg in ("1", "on"):
                relays[i].value(1)
                print("Relay " + str(i+1) + " (" + RELAY_LABELS[i] + ") ON")
            elif msg in ("0", "off"):
                relays[i].value(0)
                print("Relay " + str(i+1) + " (" + RELAY_LABELS[i] + ") OFF")
            break

# -- MQTT CONNECT --------------------------------------------
def connect_mqtt():
    client_id = ubinascii.hexlify(machine.unique_id()).decode()
    client = MQTTClient(
        client_id = client_id,
        server    = "io.adafruit.com",
        port      = 1883,
        user      = AIO_USERNAME,
        password  = AIO_KEY,
        keepalive = 60
    )
    client.set_callback(on_message)
    client.connect()
    for feed in RELAY_FEEDS:
        client.subscribe(feed)
        print("Subscribed: " + feed)
    return client

# -- MAIN ----------------------------------------------------
connect_wifi()
client = connect_mqtt()

last_publish = 0
INTERVAL     = 20

print("\nStarting main loop...\n")

while True:
    try:
        client.check_msg()

        now = time.time()
        if now - last_publish >= INTERVAL:
            sensor.measure()
            temp = sensor.temperature()
            hum  = sensor.humidity()

            client.publish(TEMP_FEED, str(temp))
            client.publish(HUM_FEED,  str(hum))

            relay_states = [r.value() for r in relays]
            print("Temp: " + str(temp) + "C  Hum: " + str(hum) + "%  Relays: " + str(relay_states))

            last_publish = now

    except OSError as e:
        print("Error: " + str(e) + " - reconnecting...")
        time.sleep(3)
        try:
            connect_wifi()
            client = connect_mqtt()
        except Exception as ex:
            print("Reconnect failed: " + str(ex))

    time.sleep(0.5)