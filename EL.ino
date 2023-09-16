#include <Wire.h>
#include<WiFi.h>
#include<FirebaseESP32.h>

//auth part
#define FIREBASE_HOST "https://console.firebase.google.com/u/0/project/smart-parking-system-19089/database/smart-parking-system-19089-default-rtdb/data/~2F"
#define FIREBASE_AUTH "AIzaSyDfXWZFmvRvLplJsd6cfeVN1MELAQ2fDnI"
#define WIFI_SSID     "Kushal"
#define WIFI_PASSWORD "kushal150803"

//sensor part
#define TRIG_1 7
#define ECHO_1 6
#define TRIG_2 15
#define ECHO_2 0
#define TRIG_3 4
#define ECHO_3 2

//database instance
FirebaseData firebaseData;
FirebaseAuth auth;
FirebaseJson json;

unsigned long sendDataPrevMillis = 0;
int intValue;
float floatValue;
bool signupOK = false;

void setup() {
  Serial.begin(115200);
  //sensor setups
  /*pinMode(TRIG_1, OUTPUT);
  pinMode(ECHO_1, INPUT);
  pinMode(TRIG_2, OUTPUT);
  pinMode(ECHO_2, INPUT);
  pinMode(TRIG_3, OUTPUT);
  pinMode(ECHO_3, INPUT);*/
  
  //WIFI and Firebase setup
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
  Firebase.setReadTimeout(firebaseData, 1000 * 60);
  Firebase.setwriteSizeLimit(firebaseData, "tiny");
  Firebase.enableClassicRequest(firebaseData, true);
  
  Serial.println("------------------------------------");
  Serial.println("Connected...");
}

void loop() {
  
  /*digitalWrite(TRIG_1, LOW);
  digitalWrite(TRIG_2, LOW);
  digitalWrite(TRIG_3, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_1, HIGH);
  digitalWrite(TRIG_2, HIGH);
  digitalWrite(TRIG_3, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_1, LOW);
  digitalWrite(TRIG_2, LOW);
  digitalWrite(TRIG_3, LOW);
  
  
  int distance1 = (pulseIn(ECHO_1, HIGH)*0.034/2);
  int distance2 = (pulseIn(ECHO_2, HIGH)*0.034/2);
  int distance3 = (pulseIn(ECHO_3, HIGH)*0.034/2);*/
  
  
  if(1){
    int data = random(0,99);
    Serial.println(data);
    json.set("/out", data);
  }
  Firebase.updateNode(firebaseData,"/Sensor",json);
  Serial.println("Working");
  delay(1000);
}
