#include <Arduino.h>

void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.println("Started");
  if(Serial.available()){
    Serial.println("There");
  }else{
    Serial.println("No");

  }
}

