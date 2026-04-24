import neopixel, machine, network, socket, json, time, gc, math

SSID     = "kritish"
PASSWORD = "pass"

N  = 8
np = neopixel.NeoPixel(machine.Pin(0), N)
BR = 0.3
current_mode  = "solid"
current_color = (0, 255, 0)
running       = True

def dim(color):
    return tuple(int(c * BR) for c in color)

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def wheel(pos):
    pos = pos % 256
    if pos < 85:   return (255-pos*3, pos*3, 0)
    if pos < 170:  pos-=85;  return (0, 255-pos*3, pos*3)
    pos-=170;      return (pos*3, 0, 255-pos*3)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting...", end="")
    for _ in range(20):
        if wlan.isconnected():
            print("\nIP:", wlan.ifconfig()[0])
            return wlan.ifconfig()[0]
        time.sleep(1); print(".", end="")
    return None

frame = 0
def animation_tick():
    global frame
    if not running:
        np.fill((0,0,0)); np.write(); return
    if current_mode == "rainbow":
        for i in range(N):
            pos = (i * 256 // N + frame * 3) & 255
            np[i] = dim(wheel(pos))
        np.write()
    elif current_mode == "breathe":
        br_val = (math.sin(frame * 0.1) + 1) / 2
        c = tuple(int(v * br_val * BR) for v in current_color)
        np.fill(c); np.write()
    else:
        np.fill(dim(current_color)); np.write()

HTML = """<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pico 2 W Control</title>
<style>
  body{font-family:sans-serif;background:#121212;color:#fff;text-align:center;padding:20px}
  .card{background:#1e1e1e;padding:25px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.7);max-width:360px;margin:auto}
  h2{color:#00e5ff;margin-bottom:20px;letter-spacing:1px}
  .section{margin-bottom:25px;text-align:left}
  label{display:block;margin-bottom:12px;font-size:14px;color:#888;text-transform:uppercase}
  input[type=color]{width:100%;height:60px;border:none;border-radius:12px;cursor:pointer;background:#333;padding:5px}
  input[type=range]{width:100%;height:8px;border-radius:5px;background:#333;outline:none;-webkit-appearance:none;margin:15px 0}
  input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;background:#00e5ff;border-radius:50%;cursor:pointer;box-shadow:0 0 10px rgba(0,229,255,0.5)}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
  button{background:#2a2a2a;color:#eee;border:1px solid #444;padding:15px;border-radius:12px;cursor:pointer;font-size:15px;transition:0.2s}
  button:active{background:#00e5ff;color:#000;transform:scale(0.95)}
  .off-btn{grid-column: span 2; background:#3d1a1a; border-color:#663333}
</style>
</head>
<body>
<div class="card">
  <h2>Pico 2 W Lab</h2>
  <div class="section">
    <label>Brightness</label>
    <input type="range" min="1" max="100" value="30" oninput="set('brightness',this.value)">
  </div>
  <div class="section">
    <label>Color Palette</label>
    <input type="color" value="#00ff00" onchange="set('color',this.value)">
  </div>
  <div class="section">
    <label>Light Effects</label>
    <div class="grid">
      <button onclick="set('mode','solid')">Solid</button>
      <button onclick="set('mode','rainbow')">Rainbow</button>
      <button onclick="set('mode','breathe')">Breathe</button>
      <button onclick="set('mode','off')" class="off-btn">Turn Off</button>
    </div>
  </div>
</div>
<script>
function set(k,v){ fetch('/set?'+k+'='+encodeURIComponent(v)); }
</script>
</body>
</html>"""

def handle(conn):
    global current_mode, current_color, BR, running
    try:
        conn.settimeout(0.5)
        req = conn.recv(1024).decode()
        if not req: return
        path = req.split(' ')[1] if ' ' in req else '/'
        if path.startswith('/set?'):
            params = path[5:]
            for p in params.split('&'):
                if '=' in p:
                    k, v = p.split('=', 1)
                    v = v.replace('%23','#')
                    if k == 'mode':
                        current_mode = v
                        running = (v != 'off')
                    elif k == 'color':
                        current_color = hex_to_rgb(v)
                    elif k == 'brightness':
                        BR = int(v) / 100
            conn.send(b"HTTP/1.1 200 OK\r\n\r\nOK")
        else:
            conn.send(b"HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n" + HTML)
    except: pass
    finally: conn.close()

ip = connect_wifi()
if ip:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(2)
    s.setblocking(False)
    print("URL: http://" + ip)
    while True:
        animation_tick()
        frame = (frame + 1) % 1000
        try:
            conn, _ = s.accept()
            handle(conn)
        except OSError: pass
        if frame % 100 == 0: gc.collect()
        time.sleep_ms(40)
