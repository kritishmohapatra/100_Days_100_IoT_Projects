from machine import ADC, Pin
import utime
import json
from umqttsimple import MQTTClient
import network

# Initialize ADC for the joystick's VRx and VRy pins
adc_x = ADC(26)
adc_y = ADC(27)

# Initialize Pin for the joystick's SW pin (button)
button = Pin(17, Pin.IN, Pin.PULL_UP)

# Configure your Wi-Fi credentials
SSID     = 'kritish'
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
TOPIC      = b'joystick'
USER      = b'userid'    # Replace with your MQTT username
PASSWORD  = b'pass'# Replace with your MQTT password

def mqtt_connect():
   client = MQTTClient(CLIENT_ID, SERVER, user=USER, password=PASSWORD, keepalive=3600)
   client.connect()
   print('Connected to %s MQTT Broker'%(SERVER))
   return client

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   utime.sleep(5)
   machine.reset()

try:
   client = mqtt_connect()
except OSError as e:
   reconnect()


while True:
   # Read X and Y coordinates
   x = adc_x.read_u16()
   y = adc_y.read_u16()

   # Read button state
   btn_state = button.value()



   # Create a dictionary to hold the data
   data = {
      'x_value': x,
      'y_value': y,
      'button_value': 'Pressed' if btn_state == 0 else 'Not Pressed'
    }

   print('X:', x, 'Y:', y, 'Button:', 'Pressed' if btn_state == 0 else 'Not pressed')

   # Convert the dictionary to a JSON string
   data_json = json.dumps(data)

   print(data_json)
   client.publish(TOPIC, data_json)

   # Delay to avoid flooding console
   utime.sleep(1)
