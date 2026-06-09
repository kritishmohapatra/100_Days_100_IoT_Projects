import machine
import time
from umqttsimple import MQTTClient
from time import sleep
import network
import neopixel

# Constants
NUM_LEDS = 8
PIN      = 0 # GPIO pin connected to WS2812

# Initialize the NeoPixel
np = neopixel.NeoPixel(machine.Pin(PIN), NUM_LEDS)

# Wi-Fi credentials
SSID       = 'id'
WPASSWORD  = 'pass'

# MQTT parameters
SERVER    = 'ip'    # Replace with your MQTT broker IP
CLIENT_ID = b'pico'
TOPIC     = b'RGB_LED_Control'
USER      = b'user'    # Replace with your MQTT username
PASSWORD  = b'pass'# Replace with your MQTT password

# MQTT Callback function
def on_message(topic, msg):
    print("Received message:", msg)
    data   = eval(msg) # Convert string message to dictionary
    red    = data['red']
    green  = data['green']
    blue   = data['blue']
    delay  = data['delay']

    # Set all LEDs to the received color
    for i in range(NUM_LEDS):
        np[i] = (red, green, blue)
    np.write()

    # Blink the LEDs with the received delay
    time.sleep_ms(delay)
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()
    time.sleep_ms(delay)

# Function to connect and subscribe to MQTT broker
def connect_and_subscribe():
    client = MQTTClient(CLIENT_ID,
                        SERVER,
                        user=USER,
                        password=PASSWORD,
                        keepalive=3600)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(TOPIC)
    return client

# Main function
def main():
    # Activate the network interface
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, WPASSWORD)

    print('Starting... Trying to connect to Wifi...')

    while not wlan.isconnected():
       pass

    print('\nConnected to Wi-Fi')
    print(wlan.ifconfig())

    client = connect_and_subscribe()
    print('Connected to broker')

    try:
        while True:
            client.check_msg()
            sleep(1)

    finally:
        client.disconnect()

# Run the main function
if __name__ == "__main__":
    main()
