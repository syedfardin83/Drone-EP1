#include <SoftwareSerial.h>

SoftwareSerial BTSerial(2,3);
String inp_str = "";
bool read_end = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(8,INPUT);
  BTSerial.begin(9600);
  Serial.begin(9600);
  delay(500);

  Serial.println("Serial Monitor ready!");
  if(digitalRead(8)){
    Serial.println("HC05 connected and paired.");
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  while(!digitalRead(8)){
    Serial.println("Connect HC05 first!");
  }
  while(BTSerial.available()){
    char ch = BTSerial.read();
    inp_str+=ch;

    if(ch=='\n'){
      read_end = true;
    }
  }
  if(read_end){
    inp_str.trim();
    Serial.println(inp_str);
    inp_str="";
    read_end=false;
  }
}
