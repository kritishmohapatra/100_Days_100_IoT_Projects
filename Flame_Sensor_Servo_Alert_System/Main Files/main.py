from machine import Pin, ADC, PWM
import time

FLAME_PIN = 34
SERVO_PIN = 18
THRESHOLD = 1000

flame = ADC(Pin(FLAME_PIN))
flame.atten(ADC.ATTN_11DB)

servo = PWM(Pin(SERVO_PIN), freq=50)

def set_angle(angle):
    duty = int((angle / 180) * 77 + 26)
    servo.duty(duty)

def sweep_0_to_180():
    for angle in range(0, 181, 5):
        set_angle(angle)
        time.sleep_ms(15)

def reset_to_0():
    set_angle(0)
    time.sleep_ms(500)

print("Flame detection system started")
set_angle(0)
time.sleep(1)

flame_active = False

while True:
    raw = flame.read()
    
    if raw < THRESHOLD and not flame_active:
        print(f"Flame detected! ADC: {raw}")
        flame_active = True
        sweep_0_to_180()
    
    elif raw >= THRESHOLD and flame_active:
        print("Flame gone, resetting")
        flame_active = False
        reset_to_0()
    
    time.sleep_ms(100)