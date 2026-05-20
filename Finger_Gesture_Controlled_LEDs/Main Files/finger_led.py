import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
import time

ser = serial.Serial('COM14', 115200, timeout=1)
time.sleep(2)

detector = HandDetector(maxHands=1)
cap = cv2.VideoCapture(0)

last_count = -1

def set_leds(count):
    for i in range(1, 6):
        cmd = f"LED{i}:{'ON' if i <= count else 'OFF'}\n"
        ser.write(cmd.encode())
        time.sleep(0.05)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hands, frame = detector.findHands(frame)

    finger_count = 0
    hand_type = ""

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        finger_count = sum(fingers)

        if hand["type"] == "Left":
            hand_type = "Right"
        else:
            hand_type = "Left"

    cv2.putText(frame, f'Fingers: {finger_count}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    cv2.putText(frame, f'Hand: {hand_type}', (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)

    cv2.imshow("Finger LED Control", frame)

    if finger_count != last_count:
        set_leds(finger_count)
        last_count = finger_count

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()