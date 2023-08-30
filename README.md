# iFaw-Project

Weather Station and Faw Counting 

## TODO List:

- [ ] MongoDB Client (store and query data api)
- [ ] FawPredict (predict faw warning level and publish to MQTT)
- [ ] Connect to Node-RED
- [ ] Complete README.md 

## Table of Contents <a name="top"></a>

1. [System Overview](#overview)

2. [System Installation](#installation)

    2.1. [Hardware](#hardware)

    2.2. [Software](#software)

      2.2.1. [Node-RED](#node-red)

      2.2.2. [MongoDB Client](#mongodb-client)

      2.2.3. [FawPredict](#fawpredict)

3. [Citation](#citation)

4. [Acknowledgements](#acknowledgements)

# 1. System Overview <a name="overview"></a>

Pending ...
# 2. System Installation <a name="installation"></a>
## 2.1. Hardware <a name="hardware"></a>

- ESP32
- GY1145
- Weather Station (DF Robot)
- Faw Counter (custom design)

### Install:
1. Install ESP32 Add-on in Arduino IDE. 

  - In Arduino IDE, go to File > Preferences. <br>
  - Copy and paste the following line to the Additional Boards Manager URLs field:<br>
  <https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json> <br>
  - Open the Boards Manager:<br>
    + You can go to Tools > Board > Boards Manager…<br>
    + Search for ESP32 and press the install button for esp32 by Arduino.<br>

2. Add SoftwareSerial Lib:<br>
  - In the menu bar, select Sketchs > Include Library > Add .Zip Library...<br>
  - Select espsoftwareserial-main.zip in Libs folder.<br>

3. Add GY1145 Libs:<br>
  - In the menu bar, select Tools > Manage Libraries…<br>
  - Search "Adafruit SI1145" and install.<br>

4. Wifi Lib:<br>
  - The PubSubClient library provides a client for doing simple publish/subscribe messaging with a server that supports MQTT (basically allows your ESP32 to talk with Node-RED).<br>
[Click here to dowload Libs](https://github.com/knolleary/pubsubclient/archive/master.zip) <br>
You should have a .zip folder in your Downloads folder
Unzip the .zip folder and you should get pubsubclient-master folder. <br>
Rename your folder from pubsubclient-master to pubsubclient. <br>
  - In the menu bar, select Sketchs > Include Library > Add .Zip Library...<br>
  - Select pubsubclient.zip.<br>
### Hardware Settings:<br>
| ESP32 | Weather | GY1145 | Counter|
| ------------- | ------------- | ------------- | -------------|
| 5V  | 5V |  x | 5V |
| 3.3V  | x |  x   | Vin |
| GND  | GND | GND | GND |
| TX2  | RX |  x | x  |
| RX2  | TX | x | x |
| SCL  | x | SCL | x |
| SDA  | x | SDA | x |
| GPIO33  | x | x | OUT |

### Upload code for ESP32:

[Code](./Hardware/SensorNode/SensorNode.ino)
## 2.2. Software <a name="software"></a>

### 2.2.1. Node-RED <a name="node-red"></a>

1. Install Node-RED: [Click here](https://nodered.org/docs/getting-started/local)
2. Import [flows.json](./Software/Node-RED/flows.json) to Node-RED
### 2.2.2. MongoDB Client <a name="mongodb-client"></a>

1. `cd Software/MongoDBClient`
2. `pip install -r requirements.txt`

### 2.2.3. FawPredict <a name="fawpredict"></a>

### Setup

1. Clone repo
2. `cd Software/FAWpredict`
3. `pip install -r requirements.txt`
4. Copy .env.example into .env and fill in the API key

### How to run

Open the terminal and type
  
    python FAWPredict.py --mode [SELECT_MODE] --location [SELECT_LOCATION] --date [SELECT_DATE] --age [SELECT_AGE]
    
- [SELECT_MODE]: `regression` mode or `lookup` mode
- [SELECT_LOCATION]: location to analyze (for example: Hanoi)
- [SELECT_DATE]: format: yyyy-mm-dd (Example: 2022-04-01)
- [SELECT_AGE]: a number from 0-8 represent for development stages of worm
```   
0: egg
1: first instar
2: second instar
3: third instar
4: fourth instar
5: fifth instar
6: sixth instar
7: larval stage
8: adult stage
```

## 3.Citation <a name="citation"></a>

## 4.Acknowledgements <a name="acknowledgements"></a>

