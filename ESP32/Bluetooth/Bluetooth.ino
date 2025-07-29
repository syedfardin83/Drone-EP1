#include "BluetoothSerial.h"
#include <math.h>

BluetoothSerial BTSerial;
String msg = "";
bool stringEnd = false;
int motor_pins[4] = {33,27,14,13};
int green_pin = 22;
int blue_pin = 23;

int throttle = 0;

String* splitBySpace(String str){
  static String words[10];int i=0;String word = "";int wordIndex = 0;
  while(i<str.length()){
    if((str[i]==' ')){
      words[wordIndex] = word;
      word="";
      wordIndex++;i++;
      continue;
    }
    if(i==str.length()-1){
      word+=str[i];
      words[wordIndex] = word;break;
    }
    word+=str[i];
    i++;
  }
  return words;
}

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
    String* commands = splitBySpace(msg);
    analogWrite(blue_pin,0);
    delay(50);
    analogWrite(green_pin,200);
    delay(50);
    analogWrite(green_pin,0);
        // throttle+=ceil(commands[3].toDouble()*5);
        Serial.print(msg);
        Serial.println("");
    msg="";
    stringEnd=false;
  }
    for(int i=0;i<4;i++){
      if(throttle<0){
              analogWrite(motor_pins[i],0);
        continue;
      }if(throttle>255){
              analogWrite(motor_pins[i],255);
        continue;
      }
      analogWrite(motor_pins[i],throttle);
      
    }
} 
