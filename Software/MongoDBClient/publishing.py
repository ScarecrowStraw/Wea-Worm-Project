# python 3.6

import random
import time
import json
from paho.mqtt import client as mqtt_client
import pymongo

broker = 'localhost'
port = 1883
topic = "pf/node001"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set("nam", "1")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    id = 0
    tem = 0
    humidity = 0
    pressusre = 0
    co2 = 0
    nh3 = 0
    ch4 = 0
    no2 = 0

    time_repeat = "day"
    time_start = "07:00:00"
    state = "off"
    month = "12"
    day = "12"
    hour = "12"
    minute = "12"

    msg_count = {
        "name_gate": "PF",# Plant Factory 404E5
        "id_device": {
            "type": "WiFi",
            "group": "A",
            "index_node": 1
        },
        "data": {
            "id": id,
            "time": {
                "mm": month,
                "dd": day,
                "h": hour,
                "m": minute
            },
            "tem": tem,
            "humidity": humidity,
            "pressusre": pressusre,
            "co2": co2,
            "nh3": nh3,
            "ch4": ch4,
            "no2": no2
        },
        "state_pump":
            {
                "state": state,
                "time_execution": {
                    "time_repeat": time_repeat,
                    "time_start": time_start
                }
            }
    }

    while True:
        time.sleep(5)
        # msg = f"messages: {msg_count}"
        msg = msg_count
        # print(type(msg))
        msg = json.dumps(msg)
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        id += 1
        tem = random.randint(5, 15)
        humidity = random.randint(5, 15)
        pressusre = random.randint(100, 105)
        co2 = random.randint(1, 5)
        nh3 = random.randint(1, 5)
        ch4 = random.randint(1, 5)
        no2 = random.randint(1, 5)
        dt = datetime.today()

        month = str(dt.month)
        day = str(dt.day)
        hour = str(dt.hour)
        minute = str(dt.minute)
        msg_count = {
            "name_gate": "PF",# Plant Factory 404E5
            "id_device": {
                "type": "WiFi",
                "group": "A",
                "index_node": 1
            },
            "data": {
                "id": id,
                "time": {
                    "mm": month,
                    "dd": day,
                    "h": hour,
                    "m": minute
                },
                "tem": tem,
                "humidity": humidity,
                "pressusre": pressusre,
                "co2": co2,
                "nh3": nh3,
                "ch4": ch4,
                "no2": no2
            },
            "state_pump":
                {
                    "state": state,
                    "time_execution": {
                        "time_repeat": time_repeat,
                        "time_start": time_start
                    }
                }
        }

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
