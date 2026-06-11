import machine
from umqttsimple import MQTTClient
from time import sleep
import network
from dht import DHT11

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

# Configure MQTT
SERVER     = 'ip'  # Replace with your MQTT broker IP
CLIENT_ID  = b'PICO'
TOPIC_TEMP = b'pico/dht11/temperature'
TOPIC_HUMD = b'pico/dht11/humidity'
USER       = b'user'    # Replace with your MQTT username
PASSWORD   = b'pass'# Replace with your MQTT password

def mqtt_connect():
   client = MQTTClient(CLIENT_ID,
                       SERVER, 
                       user=USER,
                       password=PASSWORD,
                       keepalive=3600)
   client.connect()
   print('Connected to %s MQTT Broker'%(SERVER))
   return client

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   sleep(5)
   machine.reset()

try:
   client = mqtt_connect()
except OSError as e:
   reconnect()

# Create a DHT11 instance
dht11 = DHT11(machine.Pin(18))  # the DATA pin is connected to GP2 on the Raspberry Pi Pico

while True:
    dht11.measure()  # make a new measurement
    temp  = dht11.temperature()  # read temperature
    hum   = dht11.humidity()  # read humidity
    print('Temperature:', temp, 'C', 'Humidity:', hum, '%')
    client.publish(TOPIC_TEMP, str(temp))
    client.publish(TOPIC_HUMD, str(hum))
    sleep(5)  # wait for 5 seconds
