import sys
from datetime import datetime
import configuration as config
import paho.mqtt.client as mqtt
import pymongo
from pymongo import MongoClient
import json

MQTT_HOST = '192.168.1.113'
MQTT_PORT = "1883"

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = "27017"

class MongoDBClient():
    def __init__(self):
        self.setupMongodb()
        self.setupMQTT_Iots()

    def setupMQTT_Iots(self):
         self.mqttc = mqtt.Client()
         self.mqttc.on_message = self.on_iot_message
         self.mqttc.on_publish = self.on_iot_publish

         self.host = MQTT_HOST
         self.port = MQTT_HOST

         self.mqttc.connect(self.host, 1883, 60)
         self.mqttc.subscribe([("esp32/temperature", 0), ("esp32/humidity", 0), ("esp32/barP", 0), ("esp32/Vis", 0),
                               ("esp32/winddirection", 0), ("esp32/windspeed", 0), ("esp32/rain1H", 0), ("esp32/rain1D", 0),
                               ("esp32/counter", 0), ("predictor", 0)])
         self.mqttc.loop_forever()

    def setupMongodb(self):
        self.client = MongoClient(MONGODB_HOST, int(MONGODB_PORT))

        self.db = self.client["WeatherStation"]

        print(self.db.list_collection_names())


    def on_iot_message(self, mqttc, obj, msg):
         
        if msg.topic == "esp32/temperature":
            print('Update IoTs ...')
            self.data = msg.payload
            tmp_data = {"Temperature": str(self.data)}
            collection_name = "Temperature"
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(tmp_data)
        elif msg.topic == "esp32/humidity":
            self.data = msg.payload
            tmp_data = {"Humidity": str(self.data)}
            collection_name = "Humidity"
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(tmp_data)          
        elif msg.topic == "esp32/barP":
            self.data = msg.payload
            tmp_data = {"Baro": str(self.data)}
            collection_name = "Baro"
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(tmp_data)        
        elif msg.topic == "esp32/Vis":
            self.data = msg.payload
            tmp_data = {"Brightness": str(self.data)}
            collection_name = "Brightness"
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(tmp_data)  
        elif msg.topic == "esp32/winddirection":
            self.data = msg.payload
            tmp_data = {"WindDirection": str(self.data)}
            collection_name = "WindDirection"
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(tmp_data) 
        elif msg.topic == "esp32/windspeed":
            self.data = msg.payload
            tmp_data = {"WindSpeed": str(self.data)}
            collection_name = "WindSpeed"
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(tmp_data) 
        elif msg.topic == "esp32/rain1H":
            self.data = msg.payload
            tmp_data = {"Rain1H": str(self.data)}
            collection_name = "Rain1H"
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(tmp_data) 
        elif msg.topic == "esp32/rain1D":
            self.data = msg.payload
            tmp_data = {"rain1D": str(self.data)}
            collection_name = "rain1D"
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(tmp_data) 
        elif msg.topic == "esp32/counter":
            self.data = msg.payload
            tmp_data = {"FAWCounter": str(self.data)}
            collection_name = "FAWCounter"
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(tmp_data) 
        elif msg.topic == "predictor":
            self.data = msg.payload
            tmp_data = {"FAWPredict": str(self.data).split("/")}
            # print(tmp_data)
            collection_name = "FAWPredict"
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(tmp_data) 

    def on_iot_publish(self, mqttc, obj, mid):
        # print("pub: " + str(mid) + " - mess = " + str(obj))
        pass

    def print(self, mess):
        print(mess)
        print("\n")
    