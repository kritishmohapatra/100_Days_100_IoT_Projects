
from machine import Pin, I2C
import ssd1306
import time

# ---- Configuration ----
SLOT_PINS = [32, 33]            # PIR OUT pins, one per slot
NUM_SLOTS = len(SLOT_PINS)
COOLDOWN_MS = 3000              # ignore re-triggers for this long after a toggle

# ---- OLED setup (SSD1306, I2C) ----
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ---- Sensor setup (PIR drives its own output, no pull-up needed) ----
sensors = [Pin(pin, Pin.IN) for pin in SLOT_PINS]

occupied = [False] * NUM_SLOTS
last_value = [0] * NUM_SLOTS
last_toggle_time = [0] * NUM_SLOTS


def update_display():
    oled.fill(0)
    oled.text("Parking System", 0, 0)
    oled.text("-" * 16, 0, 10)

    for i in range(NUM_SLOTS):
        label = "Slot {}: {}".format(i + 1, "FULL" if occupied[i] else "FREE")
        oled.text(label, 0, 20 + i * 10)

    free = occupied.count(False)
    oled.text("Free: {}/{}".format(free, NUM_SLOTS), 0, 20 + NUM_SLOTS * 10 + 4)
    oled.show()


def main():
    update_display()
    while True:
        now = time.ticks_ms()
        changed = False

        for i, sensor in enumerate(sensors):
            val = sensor.value()
            # Rising edge = a fresh motion event just started
            if val == 1 and last_value[i] == 0:
                if time.ticks_diff(now, last_toggle_time[i]) > COOLDOWN_MS:
                    occupied[i] = not occupied[i]
                    last_toggle_time[i] = now
                    changed = True
                    print("Slot {} toggled -> {}".format(i + 1, "FULL" if occupied[i] else "FREE"))
            last_value[i] = val

        if changed:
            update_display()
        time.sleep_ms(100)


if __name__ == "__main__":
    main()