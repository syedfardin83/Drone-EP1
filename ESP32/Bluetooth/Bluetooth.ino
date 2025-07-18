#include "BluetoothSerial.h"

BluetoothSerial BTSerial;
String msg = "";
bool stringEnd = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  BTSerial.begin("Lark");

}

void loop() {
  // put your main code here, to run repeatedly:
  if(BTSerial.available()){
    char ch = BTSerial.read();
    msg+=ch;
    if(ch=='\n'){
      stringEnd=true;
    }
  }
  if(stringEnd){
    msg.trim();
    Serial.print("BT says :");
    Serial.println(msg);

    msg="";
    stringEnd=false;
  }
} 
