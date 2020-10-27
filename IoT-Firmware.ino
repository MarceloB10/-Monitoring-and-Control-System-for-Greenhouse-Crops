//Here goes the MTTQ connetion code

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char *ssid = "name"; // Enter your WiFi name
const char *password = "pass";  // Enter WiFi password
const char *mqtt_broker = "broker.emqx.io";
const int mqtt_port = 1883;

// Set software serial baud to 115200;
Serial.begin(115200);
// connecting to a WiFi network
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
   delay(500);
   Serial.println("Connecting to WiFi..");
}

client.setServer(mqtt_broker, mqtt_port);
client.setCallback(callback);
while (!client.connected()) {
   Serial.println("Connecting to public emqx mqtt broker.....");
   if (client.connect("esp8266-client")) {
       Serial.println("Public emqx mqtt broker connected");
   } else {
       Serial.print("failed with state ");
       Serial.print(client.state());
       delay(2000);
   }
}

void callback(char *topic, byte *payload, unsigned int length) {
   Serial.print("Message arrived in topic: ");
   Serial.println(topic);
   Serial.print("Message:");
   for (int i = 0; i < length; i++) {
       Serial.print((char) payload[i]);
   }
   Serial.println();
   Serial.println("-----------------------");
}

// publish and subscribe
client.publish("esp8266/test", "hello emqx");
client.subscribe("esp8266/test");

   Serial.print("Message arrived in topic: ");
   Serial.println(topic);
   Serial.print("Message:");
   for (int i = 0; i < length; i++) {
       Serial.print((char) payload[i]);
   }
   Serial.println();
   Serial.println("-----------------------");
}


//---------------- Your Sensors/Actuators Code ---------------

#include <DHT.h>

//humidity-termperature
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

//----------------------------------------------------------
  
void setup() { 
  // start serial monitor 
  
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(3, OUTPUT);

  pinMode(8, INPUT);
  
  Serial.begin(9600);
  dht.begin();
  
} 

//-------------------------------------------------------

void loop() {  

//water level

  int valo = analogRead(A0);
    
  Serial.print("Water level: ");
  Serial.println(valo);

//relay

  int relay = 2;

  if (  digitalRead(8) == HIGH) {    
        digitalWrite(2, HIGH);  
  }
  else{
        digitalWrite(2, LOW);     
  }

//humidity temperature

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  Serial.print("Humidity: ");
  Serial.println(h);
  
  Serial.print("Temperature: ");
  Serial.println(t);

//Light sensor

    byte val=digitalRead(8);
 
    //if (  digitalRead(buttonPin) == HIGH) {    
    //    digitalWrite(ledPin, HIGH);   
    
    Serial.print("Light sensor: ");
    Serial.println(val);

//Soil Humidity

  int lect = analogRead(A2);
  Serial.print("Soil humidity: ");
  Serial.println(lect);  

//Water pump

int state1 =HIGH;
digitalWrite(3, state1);

Serial.print("light: ");
Serial.println(state1);


Serial.println("");
Serial.println("");

delay(2000);
} 