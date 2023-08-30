import sys
from datetime import datetime
import configuration as config
import paho.mqtt.client as mqtt
import pymongo
from pymongo import MongoClient
import json

MQTT_HOST = '192.168.0.104'
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
        self.mqttc.subscribe([("pf/node001", 0), ("owm/hanoi", 0), ("faw/hanoi", 0)])
        self.mqttc.loop_forever()

    def setupMongodb(self):
        self.client = MongoClient(MONGODB_HOST, int(MONGODB_PORT))

        self.db = self.client["WeatherStation"]
        # self.collection = [self.db[gates] for gates in config.gates]
        # print(self.collection)
        # self.collection.append(self.db["PF"]
        # for x in self.collection.find():
        #    print(x)

    def on_iot_message(self, mqttc, obj, msg):


        if msg.topic == "pf/node001":
            print('Update IoTs ...')
            self.data = msg.payload
            print(self.data)
            self.print("Message : " + str(self.data))
            self.data = self.convert_pf_node_data()
            res = json.loads(self.data)
            collection_name = res["name_gate"]
            self.collection = self.db[collection_name]
            self.result = self.collection.insert_one(res)
        elif msg.topic == "owm/hanoi":
            print('Update IoTs ...')
            self.data = msg.payload
            print(self.data)

            self.print("Message : " + str(self.data))
            print(self.data)
            res = json.loads(self.data)
            collection_name = res["name_gate"]
            self.collection = self.db[collection_name]

            self.result = self.collection.insert_one(res)
        # elif msg.topic == "owm/hanoi":

    def on_iot_publish(self, mqttc, obj, mid):
        # print("pub: " + str(mid) + " - mess = " + str(obj))
        pass

    def print(self, mess):
        print(mess)
        print("\n")
    def convert_pf_node_data(self):
        id = 0
        id += 1
        self.data = self.data.decode(encoding="utf-8")
        tem = self.data[(self.data.find("t") + len("t")): (self.data.find("h"))]
        humidity = self.data[(self.data.find("h") + len("h")): (self.data.find("p"))]
        print(humidity)
        pressusre = self.data[(self.data.find("p") + len("p")): (self.data.find("co2"))]
        print(pressusre)
        co2 = self.data[(self.data.find("co2") + len("co2")): (self.data.find("nh3"))]
        nh3 = self.data[(self.data.find("nh3") + len("nh3")): (self.data.find("ch4"))]
        ch4 = self.data[(self.data.find("ch4") + len("ch4")): (self.data.find("no2"))]
        no2 = self.data[(self.data.find("no2") + len("no2")): (self.data.find("b"))]
        batt = self.data[(self.data.find("b") + len("b")): (len(self.data))]
        if len(batt) > 2:
            batt = "100"
        print(batt)
        dt = datetime.today()

        month = str(dt.month)
        day = str(dt.day)
        hour = str(dt.hour)
        minute = str(dt.minute)
        time_repeat = "day"
        time_start = "07:00:00"
        state = "off"
        msg_count = {
            "name_gate": "pfs",  # Plant Factory 404E5
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
                "no2": no2,
                "battery": batt
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
        msg_count = json.dumps(msg_count)
        return msg_count
        
    def convertdata(self):
        temp = str(self.data)
        print("convert data function")
        self.id = ''
        self.sensorData = ''
        for i in range(temp.find('<')+1, temp.find('>')):
        #    print(temp[i])
            self.id = self.id + temp[i]
        for i in range(temp.find('>')+1, temp.find('*')):
            self.sensorData = self.sensorData + temp[i]
        print(self.id)
        print(self.sensorData)

        WindDirection = ''
        for i in range(1, 4):
            WindDirection = WindDirection + self.sensorData[i]
        self.windDirection = int(WindDirection)
    #    print(WindDirection)

        WindSpeedAverage = ''
        for i in range(5, 8):
            WindSpeedAverage = WindSpeedAverage + self.sensorData[i]
        self.windSpeedAverage = 0.44704*(int(WindSpeedAverage))

        WindSpeedMax = ''
        for i in range(9, 12):
            WindSpeedMax = WindSpeedMax + self.sensorData[i]
        self.windSpeedMax = 0.44704*(int(WindSpeedMax))

        Temperature = ''
        for i in range(13, 16):
            Temperature = Temperature + self.sensorData[i]
        self.temperature = (int(Temperature)-32.00)*5.00/9.00

        RainfallOneHour = ''
        for i in range(17, 20):
            RainfallOneHour = RainfallOneHour + self.sensorData[i]
        self.rainFallOneHour = (int(RainfallOneHour))*25.40*0.01

        RainfallOneDay = ''
        for i in range(21, 24):
            RainfallOneDay = RainfallOneDay + self.sensorData[i]
        self.rainFallOneDay = (int(RainfallOneDay))*25.04*0.01

        Humidity = ''
        for i in range(25, 27):
            Humidity = Humidity + self.sensorData[i]
        self.humidity = int(Humidity)

        BarPressure = ''
        for i in range(28, 33):
            BarPressure = BarPressure + self.sensorData[i]
        self.barPressure = int(BarPressure) / 10.00