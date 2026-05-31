"""
Desktop Companion Station — RETRO TERMINAL EDITION
====================================================
Hardware:
  - Raspberry Pi Pico 2W
  - OLED 1 (SSD1306 128x64) → I2C0: SDA=GP0, SCL=GP1  → Time / Date / Temp
  - OLED 2 (SSD1306 128x64) → I2C1: SDA=GP2, SCL=GP3  → Eyes / Todo

Dependencies (copy to Pico):
  - ssd1306.py  (from MicroPython-lib)
"""

import network
import socket
import utime
import ntptime
import ujson
import urandom
import urequests
from machine import I2C, Pin
import ssd1306
from config import *


TODO_FILE          = "todos.json"
WEB_PORT           = 80
WEATHER_REFRESH    = 600                  # refresh weather every 10 min

# ─────────────────────────────────────────────
# HARDWARE
# ─────────────────────────────────────────────
i2c0  = I2C(0, scl=Pin(1), sda=Pin(0), freq=400_000)
i2c1  = I2C(1, scl=Pin(3), sda=Pin(2), freq=400_000)
oled1 = ssd1306.SSD1306_I2C(128, 64, i2c0)
oled2 = ssd1306.SSD1306_I2C(128, 64, i2c1, addr=0x3c)

# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────
mode         = "eyes"
todos        = []
_temp        = None
_hum         = None
_condition   = None

hearts       = []
heart_active = False
heart_timer  = 0
HEART_INTERVAL = 120

eye_state    = "open"
eye_timer    = 0
eye_duration = 2000
cursor_blink = True
cursor_timer = 0

# ─────────────────────────────────────────────
# TODOS
# ─────────────────────────────────────────────
def load_todos():
    global todos
    try:
        with open(TODO_FILE, "r") as f:
            todos = ujson.load(f)
    except:
        todos = []

def save_todos():
    with open(TODO_FILE, "w") as f:
        ujson.dump(todos, f)

# ─────────────────────────────────────────────
# WIFI
# ─────────────────────────────────────────────
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        return wlan
    oled1.fill(0)
    oled1.text("> WIFI INIT...", 0, 0)
    oled1.show()
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    for i in range(20):
        if wlan.isconnected():
            break
        oled1.fill(0)
        oled1.text("> CONNECTING...", 0, 0)
        bar = "[" + "#" * i + " " * (19 - i) + "]"
        oled1.text(bar[:21], 0, 24)
        oled1.show()
        utime.sleep(1)
    return wlan

# ─────────────────────────────────────────────
# TIME
# ─────────────────────────────────────────────
DAYS   = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
MONTHS = ["JAN","FEB","MAR","APR","MAY","JUN",
          "JUL","AUG","SEP","OCT","NOV","DEC"]

def get_local_time():
    return utime.localtime(utime.time() + UTC_OFFSET_SEC)

def sync_ntp():
    try:
        ntptime.settime()
    except:
        pass

# ─────────────────────────────────────────────
# WEATHER — OpenWeatherMap
# ─────────────────────────────────────────────
def fetch_weather():
    global _temp, _hum, _condition
    try:
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(
            OWM_CITY, OWM_API_KEY)
        r = urequests.get(url, timeout=8)
        d = r.json()
        r.close()
        _temp      = d["main"]["temp"]
        _hum       = d["main"]["humidity"]
        _condition = d["weather"][0]["main"].upper()[:8]
        print("Weather:", _temp, _hum, _condition)
    except Exception as e:
        print("Weather error:", e)

# ─────────────────────────────────────────────
# OLED 1 — Time / Date / Weather
# ─────────────────────────────────────────────
def draw_oled1():
    global cursor_blink, cursor_timer
    t = get_local_time()
    yr, mo, day, hr, mn, sc, wd, _ = t

    time_str = "{:02d}:{:02d}:{:02d}".format(hr, mn, sc)
    date_str = "{} {} {}".format(day, MONTHS[mo-1], yr)
    temp_str = "{:.1f}C".format(_temp) if _temp is not None else "--.-C"
    hum_str  = "{:.0f}%".format(_hum)  if _hum  is not None else "--%"
    cond_str = _condition              if _condition        else "N/A"

    now_ms = utime.ticks_ms()
    if utime.ticks_diff(now_ms, cursor_timer) > 500:
        cursor_blink = not cursor_blink
        cursor_timer = now_ms
    cursor = "_" if cursor_blink else " "

    oled1.fill(0)
    oled1.hline(0, 0, 128, 1)
    oled1.text(time_str + cursor, 8, 4)
    oled1.text(time_str + cursor, 9, 4)       # bold trick
    oled1.hline(0, 14, 128, 1)
    oled1.text(">" + DAYS[wd] + " " + date_str, 0, 18)
    oled1.hline(0, 28, 128, 1)
    oled1.text("> " + temp_str + "  " + hum_str, 0, 33)
    oled1.text("> " + cond_str, 0, 43)
    oled1.hline(0, 54, 128, 1)
    wifi_ok = network.WLAN(network.STA_IF).isconnected()
    oled1.text("SYS:OK" if wifi_ok else "NO WIFI", 0, 56)
    oled1.text("PICO2W", 80, 56)
    oled1.show()

# ─────────────────────────────────────────────
# OLED 2 — Eyes
# ─────────────────────────────────────────────
def draw_eye(cx, cy, state):
    r = 12
    for dx in range(-r, r+1):
        for dy in range(-r, r+1):
            if r*r - r*2 <= dx*dx+dy*dy <= r*r+r:
                nx, ny = cx+dx, cy+dy
                if 0 <= nx < 128 and 0 <= ny < 64:
                    oled2.pixel(nx, ny, 1)
    if state == "blink":
        oled2.hline(cx-r, cy, r*2, 1)
        oled2.hline(cx-r, cy+1, r*2, 1)
        return
    px, py = 0, 0
    if state == "look_left":  px = -4
    elif state == "look_right": px = 4
    elif state == "look_up":  py = -3
    pr = 5
    for dx in range(-pr, pr+1):
        for dy in range(-pr, pr+1):
            if dx*dx+dy*dy <= pr*pr:
                nx, ny = cx+px+dx, cy+py+dy
                if 0 <= nx < 128 and 0 <= ny < 64:
                    oled2.pixel(nx, ny, 1)
    oled2.pixel(cx+px-2, cy+py-2, 0)
    oled2.pixel(cx+px-1, cy+py-2, 0)

def update_eye_state():
    global eye_state, eye_timer, eye_duration
    now = utime.ticks_ms()
    if utime.ticks_diff(now, eye_timer) > eye_duration:
        r = urandom.getrandbits(8) % 10
        if r < 4:
            eye_state, eye_duration = "open", 2000 + (urandom.getrandbits(8) % 2000)
        elif r < 6:
            eye_state, eye_duration = "blink", 150
        elif r < 8:
            eye_state, eye_duration = "look_left" if urandom.getrandbits(1) else "look_right", 800
        else:
            eye_state, eye_duration = "look_up", 600
        eye_timer = now

def draw_eyes():
    update_eye_state()
    oled2.fill(0)
    draw_eye(35, 32, eye_state)
    draw_eye(93, 32, eye_state)
    oled2.show()

# ─────────────────────────────────────────────
# OLED 2 — Heart Rain
# ─────────────────────────────────────────────
def draw_small_heart(x, y):
    pts = [(1,0),(2,0),(4,0),(5,0),
           (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),
           (0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),
           (1,3),(2,3),(3,3),(4,3),(5,3),
           (2,4),(3,4),(4,4),(3,5)]
    for dx, dy in pts:
        nx, ny = x+dx, y+dy
        if 0 <= nx < 128 and 0 <= ny < 64:
            oled2.pixel(nx, ny, 1)

def init_hearts():
    global hearts
    hearts = []
    for _ in range(6):
        hx = int(urandom.getrandbits(7)) % 118
        hy = -(int(urandom.getrandbits(5)) % 40) - 6
        hearts.append([hx, hy])

def update_hearts():
    global heart_active
    oled2.fill(0)
    all_done = True
    for h in hearts:
        h[1] += 2
        if h[1] < 64:
            all_done = False
            draw_small_heart(h[0], h[1])
    oled2.show()
    if all_done:
        heart_active = False

# ─────────────────────────────────────────────
# OLED 2 — Todo (max 4)
# ─────────────────────────────────────────────
def draw_todos():
    oled2.fill(0)
    oled2.text("> TODO LIST", 0, 0)
    oled2.hline(0, 10, 128, 1)
    if not todos:
        oled2.text("  (EMPTY)", 16, 24)
        oled2.text("> ADD FROM APP", 0, 40)
        oled2.show()
        return
    y = 14
    for item in todos[:4]:
        mark = "[X]" if item["done"] else "[ ]"
        oled2.text("{} {}".format(mark, item["text"][:12]), 0, y)
        y += 13
    oled2.show()

# ─────────────────────────────────────────────
# WEB SERVER
# ─────────────────────────────────────────────
server_sock = None

def start_server():
    global server_sock
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("", WEB_PORT))
    server_sock.listen(1)
    server_sock.setblocking(False)

def handle_request(req_str):
    global todos, mode
    lines = req_str.split("\r\n")
    if not lines: return "400", "Bad Request", "text/plain"
    parts = lines[0].split(" ")
    if len(parts) < 2: return "400", "Bad Request", "text/plain"
    method, path = parts[0], parts[1]

    if method == "GET" and path == "/":
        try:
            with open("todo.html", "r") as f:
                html = f.read()
            return "200 OK", html, "text/html"
        except Exception as e:
            print("HTML error:", e)
            return "500", "Error loading page", "text/plain"

    if method == "GET" and path == "/api/todos":
        return "200 OK", ujson.dumps(todos), "application/json"

    if method == "GET" and path.startswith("/api/mode"):
        return "200 OK", ujson.dumps({"mode": mode}), "application/json"

    if method == "POST" and path.startswith("/api/mode"):
        if "m=eyes" in path:   mode = "eyes"
        elif "m=todo" in path: mode = "todo"
        return "200 OK", ujson.dumps({"mode": mode}), "application/json"

    if method == "POST" and path.startswith("/api/add"):
        qs = path.split("?", 1)
        if len(qs) > 1:
            for param in qs[1].split("&"):
                if param.startswith("text="):
                    raw = param[5:].replace("+", " ")
                    text, i = "", 0
                    while i < len(raw):
                        if raw[i] == "%" and i+2 < len(raw):
                            text += chr(int(raw[i+1:i+3], 16)); i += 3
                        else:
                            text += raw[i]; i += 1
                    if text and len(todos) < 4:   # max 4 tasks
                        todos.append({"text": text[:20], "done": False})
                        save_todos()
        return "200 OK", ujson.dumps(todos), "application/json"

    if method == "POST" and path.startswith("/api/toggle"):
        qs = path.split("?", 1)
        if len(qs) > 1:
            for param in qs[1].split("&"):
                if param.startswith("i="):
                    try:
                        idx = int(param[2:])
                        if 0 <= idx < len(todos):
                            todos[idx]["done"] = not todos[idx]["done"]
                            save_todos()
                    except: pass
        return "200 OK", ujson.dumps(todos), "application/json"

    if method == "POST" and path.startswith("/api/delete"):
        qs = path.split("?", 1)
        if len(qs) > 1:
            for param in qs[1].split("&"):
                if param.startswith("i="):
                    try:
                        idx = int(param[2:])
                        if 0 <= idx < len(todos):
                            todos.pop(idx); save_todos()
                    except: pass
        return "200 OK", ujson.dumps(todos), "application/json"

    return "404 Not Found", "Not Found", "text/plain"

def poll_server():
    try:
        conn, addr = server_sock.accept()
        conn.settimeout(2.0)
        try:
            req = conn.recv(1024).decode("utf-8")
            status, body, ctype = handle_request(req)
            resp = "HTTP/1.1 {}\r\nContent-Type: {}; charset=utf-8\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}".format(
                status, ctype, len(body), body)
            conn.send(resp.encode("utf-8"))
        except: pass
        finally: conn.close()
    except OSError: pass

# ─────────────────────────────────────────────
# BOOT SPLASH
# ─────────────────────────────────────────────
def boot_splash():
    msgs = ["> BOOTING...", "> INIT DISPLAY", "> LOAD TODOS",
            "> WIFI CONNECT", "> NTP SYNC", "> ALL SYSTEMS GO"]
    for i, msg in enumerate(msgs):
        oled1.fill(0)
        oled1.text("COMPANION STN", 8, 0)
        oled1.hline(0, 10, 128, 1)
        for j, m in enumerate(msgs[:i+1]):
            if 14 + j*8 < 64:
                oled1.text(m, 0, 14 + j*8)
        oled1.show()
        oled2.fill(0)
        oled2.text("COMPANION STN", 4, 2)
        oled2.hline(0, 12, 128, 1)
        oled2.rect(24, 22, 22, 14, 1)
        oled2.rect(82, 22, 22, 14, 1)
        oled2.fill_rect(30, 26, 10, 6, 1)
        oled2.fill_rect(88, 26, 10, 6, 1)
        oled2.hline(44, 50, 40, 1)
        oled2.show()
        utime.sleep_ms(400)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    global heart_active, heart_timer

    boot_splash()
    load_todos()
    wlan = connect_wifi()
    sync_ntp()
    fetch_weather()

    ip = wlan.ifconfig()[0] if wlan.isconnected() else "NO WIFI"
    oled1.fill(0)
    oled1.text("> ONLINE!", 0, 0)
    oled1.hline(0, 10, 128, 1)
    oled1.text(ip, 0, 16)
    oled1.text("> OPEN IN PHONE", 0, 32)
    oled1.show()
    utime.sleep(3)

    start_server()

    last_weather = utime.time()
    last_ntp     = utime.time()

    while True:
        now = utime.time()

        if now - last_weather >= WEATHER_REFRESH:
            fetch_weather()
            last_weather = now

        if now - last_ntp >= 86400:
            sync_ntp()
            last_ntp = now

        if mode == "eyes":
            if not heart_active and (now - heart_timer) >= HEART_INTERVAL:
                heart_active = True
                heart_timer  = now
                init_hearts()

        draw_oled1()

        if mode == "todo":
            draw_todos()
        elif heart_active:
            update_hearts()
        else:
            draw_eyes()

        poll_server()
        utime.sleep_ms(80)

main()

