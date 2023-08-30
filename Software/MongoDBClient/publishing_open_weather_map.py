# python 3.6
import configuration as config
import random
import time
import json
from paho.mqtt import client as mqtt_client
import threading
import os
import time
from datetime import datetime
import pymongo

broker = 'localhost'
port = 1883
topic = "owm/hanoi"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

locations = ['Hanoi']
refresh_frequency = 60
# username = 'emqx'
# password = 'public'
import httplib2

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Weather Forecast App")

# Settings for the OpenWeatherMap API and Folium map
open_weather_map_API_key = "e191d1986171c2524f150e83549ed71a"
open_weather_API_endpoint = "http://api.openweathermap.org/"
city_names = locations

# How often do we want our app to refresh and download data


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
def get_db_open_weathermap():
    '''

    In this method, we download the 5 days and 3 hour separated data and store it in
    the mongodb database making timestamp as primary key, thus preventing duplicates

    '''
    # Initialize MongoDB client running on localhost
    client = pymongo.MongoClient('mongodb://localhost:27017/')


    # We create a collection for each city to store data w.r.t. city

    for city in city_names:
        url = open_weather_API_endpoint+"/data/2.5/weather?q="+city+"&appid="+open_weather_map_API_key
        http_initializer = httplib2.Http()
        response, content = http_initializer.request(url,'GET')
        utf_decoded_content = content.decode('utf-8')
        json_object = json.loads(utf_decoded_content)
        print(json_object)

    return json_object
def publish(client):
    id = 0
    tem = 0
    humidity = 0
    pressusre = 0
    co2 = 0
    nh3 = 0
    ch4 = 0
    no2 = 0
    weather_data = get_db_open_weathermap()
    time_repeat = "day"
    time_start = "07:00:00"
    state = "off"
    month = "12"
    day = "12"
    hour = "12"
    minute = "12"
    msg_count = {
        "name_gate": "OpenWeatherMap",#OpenWeatherMap
        "id_device": {
            "type": "WiFi",
            "group": "A",
            "index_node": 1
        },
        "data": weather_data,
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
        print(msg)
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
            "name_gate": "OpenWeatherMap",
            "id_device": {
                "type": "WiFi",
                "group": "A",
                "index_node": 1
            },
            "data": weather_data,
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
