# Wea-Worm-Project
Weather Station and Worm Counting 
## Install:
1. Install ESP32 Add-on in Arduino IDE. <br>
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
## Hardware Settings:<br>
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
