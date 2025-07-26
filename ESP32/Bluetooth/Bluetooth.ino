#include "BluetoothSerial.h"

BluetoothSerial BTSerial;
String msg = "";
bool stringEnd = false;
int motor_pins[4] = {33,27,14,13};
int green_pin = 22;
int blue_pin = 23;

void setup() {
  // put your setup code here, to run once:
  for(int i=0;i<4;i++){
    pinMode(motor_pins[i],OUTPUT);
  }
  pinMode(green_pin,OUTPUT);
  pinMode(blue_pin,OUTPUT);

  Serial.begin(9600);
  Serial.println("Serial started!");
  BTSerial.begin("Lark");

}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(green_pin,0);
  analogWrite(blue_pin,0);
  while(!BTSerial.hasClient()){
    analogWrite(blue_pin,0);
    delay(500);
    analogWrite(blue_pin,150);
    delay(500);
  }
  analogWrite(blue_pin,170);
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
    Serial.println(msg.toInt());
    for(int i=0;i<4;i++){
      analogWrite(motor_pins[i],msg.toInt());
    }
    analogWrite(blue_pin,0);
    analogWrite(green_pin,200);
    delay(200);
    analogWrite(green_pin,0);
    msg="";
    stringEnd=false;
  }
} 
