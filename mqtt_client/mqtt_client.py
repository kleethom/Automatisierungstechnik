import sys

print(sys.path)

import json
import paho.mqtt.client as mqtt

from database.transform import process_message

def start():

    client.connect(broker, port)

    client.subscribe(topic)

    print("Warte auf MQTT-Daten...")

    client.loop_forever()

broker = "158.180.44.197"
port = 1883
topic = "aut/SoSe26/learning_factory_simulation/#"

def on_message(client, userdata, message):

    topic = message.topic
    payload = json.loads(message.payload.decode())

    process_message(topic, payload)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.username_pw_set("bobm", "letmein")

client.on_message = on_message

