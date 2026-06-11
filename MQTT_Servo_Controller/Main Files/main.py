from machine import Pin, PWM
from time import sleep
from umqttsimple import MQTTClient
import network

# Define the GPIO pin and the frequency (50Hz is common for servo motors)
GPIO_PIN = 18
FREQ     = 50

# Create a PWM object
pwm = PWM(Pin(GPIO_PIN))

# Set the PWM frequency
pwm.freq(FREQ)

def set_angle(angle):
    # Duty cycle for servo is between 2.5% (0 degrees) and 12.5% (180 degrees)
    duty = 2.5 + (angle / 180) * 10
    # Update duty cycle
    pwm.duty_u16(int(duty * 65535 / 100))


# Configure your Wi-Fi credentials
SSID     = 'ssid'
PASSWORD = 'pass'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print(wlan.ifconfig())

# Setup MQTT
SERVER    = 'ip'  # Replace with your MQTT broker IP
CLIENT_ID = b'PICO'
TOPIC     = b'servo_angle'
USER      = b'user'    # Replace with your MQTT username
PASSWORD  = b'pass'# Replace with your MQTT password

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   sleep(5)
   machine.reset()

def on_message(topic, msg):
    angle = int(msg.decode())
    print("Received message:", angle)
    set_angle(angle)
    sleep(0.5)

def main(server, topic, username, passw):
    client = MQTTClient(CLIENT_ID,
                        server,
                        user=username,
                        password=passw,
                        keepalive=3600)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(topic)
    print("Connected to %s, subscribed to %s topic" % (server, topic))

    try:
        while True:
            client.check_msg()
            sleep(1)

    finally:
        client.disconnect()

main(SERVER, TOPIC, USER, PASSWORD)
