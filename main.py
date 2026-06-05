from threading import Thread

from mqtt_client.mqtt_client import start as mqtt_start
from visualisierung.visualisierung import start_visualisierung

mqtt_thread = Thread(
    target=mqtt_start,
    daemon=True
)

mqtt_thread.start()

start_visualisierung()