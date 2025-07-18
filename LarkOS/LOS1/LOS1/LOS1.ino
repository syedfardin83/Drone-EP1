//Lark Operating System - 1
// Only one degree of freedom (throttle control only)
// Main tasks:
// 1. Take bluetooth input
// 2. Power Motors

#include "BluetoothSerial.h"
BluetoothSerial SerialBT;

//Motor pins
#define M1_PIN NULL
#define M2_PIN NULL
#define M3_PIN NULL
#define M4_PIN NULL

//Bluetooth name
#define bt_name "ESP32";

String inputString = "";
bool stringEnd = false;

void setup() {
  //Initialize all pins
  pinMode(M1_PIN, OUTPUT);
  pinMode(M2_PIN, OUTPUT);
  pinMode(M3_PIN, OUTPUT);
  pinMode(M4_PIN, OUTPUT);

  //Initialize Serial
  SerialBT.begin(bt_name);
  Serial.begin(115200);
}

void loop() {
  if(Serial.available()){
    char ch = Serial.read();
    if (ch == '\n') {
      stringEnd = true;
    } else {
      inputString += ch;
    }
  }
  if(stringEnd){
        inputString.trim();

        analogWrite(M1_PIN,inputString.toInt());
        analogWrite(M2_PIN,inputString.toInt());
        analogWrite(M3_PIN,inputString.toInt());
        analogWrite(M4_PIN,inputString.toInt());


        inputString = "";
        stringEnd = false;
  }

}
