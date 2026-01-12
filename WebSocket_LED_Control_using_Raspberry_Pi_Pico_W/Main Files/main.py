import socket
import network
import time
from machine import Pin
import ubinascii
import uhashlib

# ---------------- LED SETUP ----------------
led = Pin(15, Pin.OUT)     # onboard LED ke liye: Pin("LED", Pin.OUT)
led.value(0)

# ---------------- WIFI ----------------
SSID = "kritish"
PASSWORD = "@Krrs2069"

# ---------------- WEBSOCKET ACCEPT KEY ----------------
def websocket_accept(key):
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    sha1 = uhashlib.sha1((key + GUID).encode()).digest()
    return ubinascii.b2a_base64(sha1).strip().decode()

# ---------------- WEBSOCKET FRAME DECODE (MASK FIX) ----------------
def ws_decode(data):
    payload_len = data[1] & 127

    if payload_len == 126:
        mask_start = 4
        data_start = 8
    elif payload_len == 127:
        mask_start = 10
        data_start = 14
    else:
        mask_start = 2
        data_start = 6

    mask = data[mask_start:mask_start + 4]
    payload = data[data_start:data_start + payload_len]

    decoded = bytearray()
    for i in range(payload_len):
        decoded.append(payload[i] ^ mask[i % 4])

    return decoded.decode()

# ---------------- WIFI CONNECT ----------------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(1)

ip = wlan.ifconfig()[0]
print("Connected!")
print("Pico IP:", ip)

# ---------------- SOCKET SERVER ----------------
server = socket.socket()
server.bind(("0.0.0.0", 80))
server.listen(1)
print("WebSocket server started")

# ---------------- CLIENT CONNECT ----------------
conn, addr = server.accept()
print("Client connected from", addr)

request = conn.recv(1024).decode()
ws_key = request.split("Sec-WebSocket-Key: ")[1].split("\r\n")[0]
accept_key = websocket_accept(ws_key)

# ---------------- HANDSHAKE RESPONSE ----------------
conn.send(
    "HTTP/1.1 101 Switching Protocols\r\n"
    "Upgrade: websocket\r\n"
    "Connection: Upgrade\r\n"
    f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
)

print("WebSocket handshake done")

# ---------------- MAIN LOOP ----------------
while True:
    data = conn.recv(1024)
    if not data:
        break

    try:
        msg = ws_decode(data)
        print("Received:", msg)

        if msg == "ON":
            led.value(1)
            reply = "LED ON"
        elif msg == "OFF":
            led.value(0)
            reply = "LED OFF"
        else:
            reply = "Send ON or OFF"

        frame = bytearray([0x81, len(reply)]) + reply.encode()
        conn.send(frame)

    except Exception as e:
        print("Error:", e)

