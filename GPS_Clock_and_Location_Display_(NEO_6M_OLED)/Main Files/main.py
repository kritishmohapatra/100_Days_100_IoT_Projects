from machine import UART, I2C, Pin
import ssd1306
import time

# ── Hardware Setup ──────────────────────────────────────────────
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
i2c  = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ── NMEA Parsers ────────────────────────────────────────────────
def parse_gprmc(sentence):
    """Parse $GPRMC for time, status, lat, lon, speed."""
    try:
        parts = sentence.split(',')
        if len(parts) < 9 or parts[2] != 'A':   # 'A' = valid fix
            return None
        raw_time  = parts[1]       # HHMMSS.ss
        raw_lat   = parts[3]       # DDMM.mmmm
        lat_dir   = parts[4]       # N/S
        raw_lon   = parts[5]       # DDDMM.mmmm
        lon_dir   = parts[6]       # E/W
        speed_kts = parts[7]       # knots

        # Time → IST (UTC + 5:30)
        hh = int(raw_time[0:2])
        mm = int(raw_time[2:4])
        ss = int(raw_time[4:6])
        total_min = hh * 60 + mm + 330       # +5h30m
        ist_h = (total_min // 60) % 24
        ist_m = total_min % 60

        # Lat/Lon decimal degrees
        lat_d = float(raw_lat[:2])  + float(raw_lat[2:])  / 60
        lon_d = float(raw_lon[:3])  + float(raw_lon[3:])  / 60
        if lat_dir == 'S': lat_d = -lat_d
        if lon_dir == 'W': lon_d = -lon_d

        speed_kmh = float(speed_kts) * 1.852 if speed_kts else 0.0

        return {
            'time': f"{ist_h:02d}:{ist_m:02d}:{ss:02d}",
            'lat':  lat_d,
            'lon':  lon_d,
            'spd':  speed_kmh,
        }
    except Exception:
        return None


def parse_gpgga(sentence):
    """Parse $GPGGA for satellite count and altitude."""
    try:
        parts = sentence.split(',')
        if len(parts) < 10 or parts[6] == '0':
            return None
        sats = int(parts[7])
        alt  = float(parts[9]) if parts[9] else 0.0
        return {'sats': sats, 'alt': alt}
    except Exception:
        return None


def verify_checksum(sentence):
    """Return True if NMEA checksum is valid."""
    try:
        if sentence[0] == '$' and '*' in sentence:
            data, chk = sentence[1:].split('*')
            calc = 0
            for c in data:
                calc ^= ord(c)
            return calc == int(chk.strip(), 16)
    except Exception:
        pass
    return False


# ── Display Helpers ─────────────────────────────────────────────
def show_searching():
    oled.fill(0)
    oled.text("GPS Clock", 24, 0)
    oled.hline(0, 10, 128, 1)
    oled.text("Searching...", 16, 28)
    oled.text("Point antenna", 8, 42)
    oled.text("to open sky", 16, 52)
    oled.show()


def show_data(gps, extra):
    oled.fill(0)

    # Line 0: Time (big-ish, centered)
    t = gps['time']
    oled.text(t, 28, 0)
    oled.hline(0, 10, 128, 1)

    # Line 1-2: Lat / Lon
    oled.text(f"Lat:{gps['lat']:9.5f}", 0, 14)
    oled.text(f"Lon:{gps['lon']:9.5f}", 0, 24)

    # Line 3: Speed
    oled.text(f"Spd:{gps['spd']:5.1f}km/h", 0, 38)

    # Line 4: Sats + Altitude
    if extra:
        oled.text(f"Sat:{extra['sats']}  Alt:{extra['alt']:.0f}m", 0, 52)
    else:
        oled.text("Acquiring sat...", 0, 52)

    oled.show()


# ── Main Loop ───────────────────────────────────────────────────
gps_data   = None
extra_data = None
buf        = b''

show_searching()
print("Waiting for GPS fix...")

while True:
    if uart.any():
        buf += uart.read(uart.any())

        while b'\n' in buf:
            line, buf = buf.split(b'\n', 1)
            try:
                sentence = line.decode('ascii').strip()
            except Exception as e:
                print("DECODE ERR:", e)
                continue

            if not sentence.startswith('$'):
                continue

            if not verify_checksum(sentence):
                continue

            if sentence.startswith('$GPRMC') or sentence.startswith('$GNRMC'):
                parsed = parse_gprmc(sentence)
                if parsed:
                    gps_data = parsed

            elif sentence.startswith('$GPGGA') or sentence.startswith('$GNGGA'):
                parsed = parse_gpgga(sentence)
                if parsed:
                    extra_data = parsed

            # Refresh display whenever we have a fix
            if gps_data:
                show_data(gps_data, extra_data)

    time.sleep_ms(50)