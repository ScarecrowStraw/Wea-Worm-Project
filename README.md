# Wea-Worm-Project
Weather Station and Worm Counting 
## Install:
1. Install ESP32 Add-on in Arduino IDE. <br>
  _ In Arduino IDE, go to File > Preferences. <br>
  _ Copy and paste the following line to the Additional Boards Manager URLs field:<br>
  <https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json> <br>
  _ Open the Boards Manager:<br>
    _ You can go to Tools > Board > Boards Manager…<br>
    _ Search for ESP32 and press the install button for esp32 by Arduino.<br>
2. Add SorfwareSerial Lib:<br>
  _ In the menu bar, select Sketchs > Include Library > Add .Zip Library...<br>
  _ Select espsoftwareserial-main.zip in Libs folder.<br>
3. Add GY1145 Libs:<br>
  _ In the menu bar, select Tools > Manage Libraries…<br>
  _ Search "Adafruit SI1145" and install.<br>
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
