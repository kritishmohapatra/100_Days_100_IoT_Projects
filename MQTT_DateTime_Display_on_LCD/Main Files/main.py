# Import necessary modules
from machine import I2C, Pin
from i2c_lcd import I2cLcd
from umqttsimple import MQTTClient
import ujson
import network
import time

# I2C parameters
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

# Scan for available I2C devices and get the first one
I2C_ADDR = i2c.scan()[0]

# Create LCD instance
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Wi-Fi credentials
SSID     = 'ssid'
PASSWORD = 'pass'

print('Starting...')

# Activate the network interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)

print('Trying to connect to Wifi...')

# Wait until connection is established
while not wlan.isconnected():
    print('.', end='')
    time.sleep(1)
    pass

print('\nConnected to Wi-Fi')
print(wlan.ifconfig())

# MQTT parameters
SERVER = 'ip'  # Replace with your MQTT broker IP
CLIENT_ID = b'pico'
TOPIC     = b'datetime'
USER      = b'user'    # Replace with your MQTT username
PASSWORD  = b'pass'# Replace with your MQTT password

# Callback function for MQTT subscriptions
def sub_cb(topic, msg):
    # Decode and load JSON message
    datetime = ujson.loads(msg)

    # Extract date and time from JSON
    date = datetime["date"]
    time = datetime["time"]

    # Print date and time on LCD
    lcd.move_to(0, 0)    # Move to first row
    lcd.putstr(date)     # Display date

    lcd.move_to(0, 1)    # Move to second row
    lcd.putstr(time)     # Display time

# Function to connect and subscribe to MQTT broker
def connect_and_subscribe():
    client = MQTTClient(CLIENT_ID, SERVER, user=USER, password=PASSWORD, keepalive=3600)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(TOPIC)
    return client

# Main function
def main():
    client = connect_and_subscribe()

    # Keep waiting and processing MQTT messages
    while True:
        client.wait_msg()

main()
