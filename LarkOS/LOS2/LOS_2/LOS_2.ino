//LOS 2.0 - FreeRTOS Based 6dof, bluetooth controlled Lark Firmware
//Three main tasks
//1. Bluetooth Input
//2. MPU6050 Sensor input and processing
//3. PID

//  Importing modules
#include "BluetoothSerial.h"
#include <math.h>

//  Defining App CPU  
#if CONFIG_FREERTOS_UNICORE
static const int app_cpu = 0;
#else
static const int app_cpu = 1;
#endif

//  Software Objects
BluetoothSerial SerialBT;

//  BT read variables
String inputString = "";
bool stringEnd = false;
char ch;

// Drone control variables
double desiredAngles[3] = {0,0,0};
double throttleIncrement = 0;
double throttle = 0;


#define bt_name "LOS 2.0"

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

void BT_update_task(void *param){
  Serial.println("Entered the bluetooth task");
  int i;
  while(1){
    if(SerialBT.available()){
      ch = SerialBT.read();
      if(ch=='\n'){
        stringEnd = true;
        inputString.trim();
      }else{
        inputString+=ch;
      }
    }
    if(stringEnd){
      String* commands = splitBySpace(inputString);

      //Update desired angles
      for(i=0;i<3;i++){
        desiredAngles[i] = radians(commands[i].toDouble());
      }
      throttleIncrement = commands[3].toDouble();
      throttle+=throttleIncrement;
      throttleIncrement = 0;

      for(i=0;i<3;i++){
        Serial.print(degrees(desiredAngles[i]));
        Serial.print("  ");
      }
      Serial.println(throttle);

      inputString = "";
      stringEnd = false;
    }
  }
}


void setup() {

  SerialBT.begin(bt_name);
  Serial.begin(115200);
  delay(100);

  //Create and run BT task
  xTaskCreatePinnedToCore(
    BT_update_task,
    "Bluetooth read and update",
    2048,
    NULL,
    1,
    NULL,
    app_cpu
  );
  

}

void loop() {
}
