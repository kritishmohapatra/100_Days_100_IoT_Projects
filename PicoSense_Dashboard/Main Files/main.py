
import network
import time
import ujson
from machine import Pin
import dht
from umqttsimple import MQTTClient

# ---------- CONFIG ----------
WIFI_SSID = "ssid"
WIFI_PASSWORD = "pass"

MQTT_BROKER = "ip"      # <-- your laptop IP (update if it changes)
MQTT_PORT = 1883
MQTT_CLIENT_ID = "pico2w_01"

TOPIC_SENSOR = b"pico/sensor/dht11"
TOPIC_LED1_CMD = b"pico/led1/cmd"
TOPIC_LED2_CMD = b"pico/led2/cmd"

PUBLISH_INTERVAL = 3  # seconds

# ---------- HARDWARE ----------
sensor = dht.DHT11(Pin(15))
led1 = Pin(16, Pin.OUT)
led2 = Pin(17, Pin.OUT)

led1.value(0)
led2.value(0)


# ---------- WIFI ----------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print("WiFi connected:", wlan.ifconfig())
        return True
    print("WiFi connection failed")
    return False


# ---------- MQTT CALLBACK ----------
def on_message(topic, msg):
    print("Received:", topic, msg)
    if topic == TOPIC_LED1_CMD:
        led1.value(1 if msg == b"ON" else 0)
    elif topic == TOPIC_LED2_CMD:
        led2.value(1 if msg == b"ON" else 0)


# ---------- MAIN ----------
def main():
    if not connect_wifi():
        return

    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(TOPIC_LED1_CMD)
    client.subscribe(TOPIC_LED2_CMD)
    print("MQTT connected to", MQTT_BROKER)

    last_publish = time.time()

    while True:
        try:
            client.check_msg()  # non-blocking check for LED commands

            if time.time() - last_publish >= PUBLISH_INTERVAL:
                try:
                    sensor.measure()
                    temp = sensor.temperature()
                    humidity = sensor.humidity()
                    payload = ujson.dumps({"temp": temp, "humidity": humidity})
                    client.publish(TOPIC_SENSOR, payload)
                    print("Published:", payload)
                except OSError as e:
                    print("DHT11 read error:", e)

                last_publish = time.time()

            time.sleep(0.2)

        except OSError as e:
            print("MQTT/network error:", e)
            time.sleep(2)
            try:
                client.connect()
                client.subscribe(TOPIC_LED1_CMD)
                client.subscribe(TOPIC_LED2_CMD)
            except OSError:
                pass


if __name__ == "__main__":
    main()
