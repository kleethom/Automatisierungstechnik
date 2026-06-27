from threading import Thread
import time

from mqtt_client.mqtt_client import start as mqtt_start


mqtt_thread = Thread(
    target=mqtt_start,
    daemon=True
)

mqtt_thread.start()

print("MQTT läuft. Liveplot separat im Jupyter Notebook starten.")

while True:
    time.sleep(1)