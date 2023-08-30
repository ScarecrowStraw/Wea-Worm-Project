#include <WiFi.h>
#include <PubSubClient.h>
#include <SoftwareSerial.h>
#include <string.h>
#include "Adafruit_SI1145.h"


Adafruit_SI1145 uv = Adafruit_SI1145();
SoftwareSerial mySerial(16, 17); // RX, TX
const char* ssid = "Fatlab";
const char* password = "12345678@!";
// Add your MQTT Broker IP address, example:
//const char* mqtt_server = "192.168.1.144";
const char* mqtt_server = "192.168.1.113";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;


char                 databuffer[35];
double               temp;
volatile int counter;
//-------------------------------------------------------
void getBuffer()      //Get weather status data
{
  int index;
  for (index = 0; index < 35; index ++)
  {
    if (mySerial.available())
    {
      databuffer[index] = mySerial.read();
      if (databuffer[0] != 'c')
      {
        index = -1;
      }
    }
    else
    {
      index --;
    }
  }
}
//-------------------------------------------------------
int transCharToInt(char *_buffer, int _start, int _stop)                             //char to int）
{
  int _index;
  int result = 0;
  int num = _stop - _start + 1;
  int _temp[num];
  for (_index = _start; _index <= _stop; _index ++)
  {
    _temp[_index - _start] = _buffer[_index] - '0';
    result = 10 * result + _temp[_index - _start];
  }
  return result;
}
//-------------------------------------------------------
int transCharToInt_T(char *_buffer)
{
  int result = 0;
  if (_buffer[13] == '-') {
    result = 0 - (((_buffer[14] - '0') * 10) + (_buffer[15] - '0'));
  }
  else {
    result = ((_buffer[13] - '0') * 100) + ((_buffer[14] - '0') * 10) + (_buffer[15] - '0');
  }
  return result;
}
//-------------------------------------------------------
int WindDirection()                                                                  //Wind Direction
{
  return transCharToInt(databuffer, 1, 3);
}
//-------------------------------------------------------
float WindSpeedAverage()                                                             //air Speed (1 minute)
{
  temp = 0.44704 * transCharToInt(databuffer, 5, 7);
  return temp;
}
//-------------------------------------------------------
float WindSpeedMax()                                                                 //Max air speed (5 minutes)
{
  temp = 0.44704 * transCharToInt(databuffer, 9, 11);
  return temp;
}
//-------------------------------------------------------
float Temperature()                                                                  //Temperature ("C")
{
  temp = (transCharToInt_T(databuffer) - 32.00) * 5.00 / 9.00;
  return temp;
}
//-------------------------------------------------------
float RainfallOneHour()                                                              //Rainfall (1 hour)
{
  temp = transCharToInt(databuffer, 17, 19) * 25.40 * 0.01;
  return temp;
}
//-------------------------------------------------------
float RainfallOneDay()                                                               //Rainfall (24 hours)
{
  temp = transCharToInt(databuffer, 21, 23) * 25.40 * 0.01;
  return temp;
}
//-------------------------------------------------------
int Humidity()                                                                       //Humidity
{
  return transCharToInt(databuffer, 25, 26);
}
//-------------------------------------------------------
float BarPressure()              //Barometric Pressure
{
  temp = transCharToInt(databuffer, 28, 32);
  return temp / 10.00;
}
//-------------------------------------------------------
void  counting(){
  counter+=1;
  //Serial.println(counter);
  
}
//-------------------------------------------------------
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
//-------------------------------------------------------
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
//-------------------------------------------------------
void setup()
{
  Serial.begin(115200);
  attachInterrupt(33,counting,RISING);
  counter=0;
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  if (! uv.begin()) {
    Serial.println("Didn't find Si1145");
    while (1);
  }
  mySerial.begin(9600);
}
//-------------------------------------------------------
void ReadAndPublishData(){
  float temperature = Temperature();
  char tempString[8];
  dtostrf(temperature, 1, 2, tempString);
  client.publish("esp32/temperature", tempString);

  float humid = Humidity();
  char humidString[8];
  dtostrf(humid, 1, 2, humidString);
  client.publish("esp32/humidity", humidString);

  float windD = WindDirection();
  char windDString[8];
  dtostrf(windD, 1, 2, windDString);
  client.publish("esp32/winddirection", windDString);
    
  float windS = WindSpeedAverage();
  char windSString[8];
  dtostrf(windS, 1, 2, windSString);
  client.publish("esp32/windspeed", windSString);

  float rain1H = RainfallOneHour();
  char rain1HString[8];
  dtostrf(rain1H, 1, 2, rain1HString);
  client.publish("esp32/rain1H", rain1HString);


  float rain1D = RainfallOneDay();
  char rain1DString[8];
  dtostrf(rain1D, 1, 2, rain1DString);
  client.publish("esp32/rain1D", rain1DString);

  float barPress = BarPressure();
  char barPString[8];
  dtostrf(barPress, 1, 2, barPString);
  client.publish("esp32/barP", barPString);
  
  float UVindex = uv.readUV();
  // the index is multiplied by 100 so to get the
  // integer index, divide by 100!
  UVindex /= 100.0; 
  
  float Vis = uv.readVisible();
  char VisString[8];
  dtostrf(Vis, 1, 2, VisString);
  client.publish("esp32/Vis", VisString);

  float IR = uv.readIR();
  char IRString[8];
  dtostrf(IR, 1, 2, IRString);
  client.publish("esp32/IR", IRString);

  float UV = uv.readUV();
  char UVString[8];
  dtostrf(UV, 1, 2, UVString);
  client.publish("esp32/UV", UVString);

  char countString[8];
  dtostrf(counter, 1, 2, countString);
  client.publish("esp32/counter", countString);
  Serial.println(counter);
}
//-------------------------------------------------------
// Main programe
void loop()
{ 
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  getBuffer();
  
  ReadAndPublishData();
  delay(1000);
}
//-------------------------------------------------------
