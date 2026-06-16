
import streamlit as st
import paho.mqtt.client as mqtt
import json
import time
import threading
from collections import deque
from datetime import datetime

# ---------- CONFIG ----------
MQTT_BROKER = "ip"   # <-- your laptop IP (same as Pico config)
MQTT_PORT = 1883

TOPIC_SENSOR = "pico/sensor/dht11"
TOPIC_LED1_CMD = "pico/led1/cmd"
TOPIC_LED2_CMD = "pico/led2/cmd"

MAX_POINTS = 50

st.set_page_config(page_title="PicoSense Dashboard", page_icon="🌡️", layout="wide")

# ---------- SHARED STATE ----------
# NOTE: The MQTT client runs in a background thread, which CANNOT access
# st.session_state (Streamlit limitation - session_state only works in the
# main script thread). We use st.cache_resource to get ONE persistent
# object (lock + shared dict + client) that survives Streamlit script reruns.


class SharedState:
    def __init__(self):
        self.lock = threading.Lock()
        self.history = deque(maxlen=MAX_POINTS)
        self.latest = {"temp": None, "humidity": None, "time": None}


@st.cache_resource
def get_shared_state():
    return SharedState()


state = get_shared_state()


# ---------- MQTT CLIENT (background thread) ----------
def on_connect(client, userdata, flags, rc, properties=None):
    print("MQTT connected, rc =", rc)
    client.subscribe(TOPIC_SENSOR)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        temp = payload.get("temp")
        humidity = payload.get("humidity")
        ts = datetime.now().strftime("%H:%M:%S")

        with state.lock:
            state.latest = {"temp": temp, "humidity": humidity, "time": ts}
            state.history.append({"time": ts, "temp": temp, "humidity": humidity})
    except Exception as e:
        print("Error parsing message:", e)


@st.cache_resource
def start_mqtt():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    return client


client = start_mqtt()

# ---------- UI ----------
st.title("🌡️ PicoSense Dashboard")
st.caption(f"Pico 2W → MQTT ({MQTT_BROKER}:{MQTT_PORT}) → Streamlit")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Live Readings")
    with state.lock:
        latest = dict(state.latest)
        history_snapshot = list(state.history)

    if latest["temp"] is not None:
        m1, m2 = st.columns(2)
        m1.metric("Temperature", f"{latest['temp']} °C")
        m2.metric("Humidity", f"{latest['humidity']} %")
        st.caption(f"Last update: {latest['time']}")
    else:
        st.info("Waiting for data from Pico 2W...")

    if len(history_snapshot) > 0:
        chart_data = history_snapshot
        st.line_chart(
            {
                "Temperature (°C)": [d["temp"] for d in chart_data],
                "Humidity (%)": [d["humidity"] for d in chart_data],
            }
        )

with col2:
    st.subheader("LED Control")

    led1_col, led2_col = st.columns(2)

    with led1_col:
        st.write("**LED 1**")
        if st.button("Turn ON 🟢", key="led1_on"):
            client.publish(TOPIC_LED1_CMD, "ON")
            st.toast("LED1 ON command sent")
        if st.button("Turn OFF ⚪", key="led1_off"):
            client.publish(TOPIC_LED1_CMD, "OFF")
            st.toast("LED1 OFF command sent")

    with led2_col:
        st.write("**LED 2**")
        if st.button("Turn ON 🟢", key="led2_on"):
            client.publish(TOPIC_LED2_CMD, "ON")
            st.toast("LED2 ON command sent")
        if st.button("Turn OFF ⚪", key="led2_off"):
            client.publish(TOPIC_LED2_CMD, "OFF")
            st.toast("LED2 OFF command sent")

# Auto-refresh every 2 seconds to show new sensor data
time.sleep(2)
st.rerun()