import network
import time
import urequests

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

INTERVAL = 10  # seconds between jokes, change as needed

while True:
  resp = urequests.get("https://v2.jokeapi.dev/joke/Programming")
  joke_dict = resp.json()
  resp.close()

  print("Here's a joke!")
  if 'joke' in joke_dict:
    print(joke_dict['joke'])
  else:
    print(joke_dict['setup'])
    print(joke_dict['delivery'])

  print()
  time.sleep(INTERVAL)