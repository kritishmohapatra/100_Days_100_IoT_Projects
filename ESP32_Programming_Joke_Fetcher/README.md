# ESP32 Programming Joke Fetcher

A MicroPython project for ESP32 that connects to WiFi and fetches a random programming joke from JokeAPI at a fixed interval, printing it to the serial console.
## Simulate on Wokwi

[![Open in Wokwi](https://img.shields.io/badge/Open%20in-Wokwi-green?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMiAxNWwtNS01IDEuNDEtMS40MUwxMCAxNC4xN2w3LjU5LTcuNTlMMTkgOGwtOSA5eiIvPjwvc3ZnPg==)](https://wokwi.com/projects/467057213270664193)

---
## How it works

The board connects to WiFi once at startup. After that, it enters an infinite loop where it sends an HTTP GET request to JokeAPI's Programming category every `INTERVAL` seconds, parses the JSON response, and prints either a single-line joke or a setup/delivery pair depending on the joke type returned.

## Hardware

- ESP32 (simulated on Wokwi, no external components required)

## Files

- `main.py` - main script: WiFi connection and the joke fetch loop

## Setup (Wokwi)

1. Create a new "ESP32 + MicroPython" project on Wokwi.
2. Replace the default `main.py` with the one in this repo.
3. Run the simulation. WiFi connects automatically using Wokwi's built-in `Wokwi-GUEST` network.
4. Jokes will print to the serial monitor every 10 seconds by default.

## Customization

Change the `INTERVAL` variable in `main.py` to control how often a new joke is fetched (value is in seconds).

## API used

[JokeAPI v2](https://v2.jokeapi.dev/) - Programming category, no API key required.


##  Author

**Kritish Mohapatra**  
B.Tech Electrical Engineering (3rd Year)  
IoT | Embedded Systems | MicroPython | ESP32  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and feel free to fork it!

Happy hacking 🚀

