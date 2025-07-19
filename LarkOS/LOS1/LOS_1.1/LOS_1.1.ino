//Lark OS 1.1
// six degrees of freedom (input from joystick)
// Main tasks:
// 1. Take bluetooth input
// 2. Read sensor data
// 3. Run PID

#include "BluetoothSerial.h"
#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <math.h>

// Software Objects
BluetoothSerial SerialBT;
Adafruit_MPU6050 mpu;

// Motor pins
int motor_pins[4] = {12,13,14,27};

// Sensor orientation
#define orientation 2

// Indicator Pins
#define LED_R_PIN NULL
#define LED_G_PIN NULL
#define LED_B_PIN NULL
#define BUZZER_PIN NULL

// MPU6050 pins
#define SCL_PIN 26
#define SDA_PIN 25

// Test button
#define BTN_PIN NULL

// Bluetooth name
#define bt_name "LOS 1.1"

// Serial reading variables
String inputString = "";
bool stringEnd = false;

// Drone control variables
double desiredAngles[3] = {0,0,0};
double throttleIncrement = 0;
double throttle = 0;
double currentAngles[3] = {0,0,0};
double* offsets;
double* data;
double integratedAngles[3] = {0,0,0};
double accAngles[3] = {0,0,0};
double alpha = 0.98;

// Time variables
unsigned long previous_time = 0;
unsigned long current_time = 0;
double dt;

// PID variables
double P=0.001,I=0.01,D=0.01;
double P_terms[3] = {0,0,0};
double I_terms[3] = {0,0,0};
double D_terms[3] = {0,0,0};
double current_errors[3] = {0,0,0};
double previous_errors[3] = {0,0,0};
double rate_outputs[3] = {0,0,0};

// Motor inputs
int motor_inputs[4] = {0,0,0,0};

double* getData(){
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  static double arr[6];
  arr[0] = a.acceleration.x;
  arr[1] = a.acceleration.y;
  arr[2] = a.acceleration.z;

  arr[3] = g.gyro.x;
  arr[4] = g.gyro.y;
  arr[5] = g.gyro.z;
  return arr;
  // AccX = a.acceleration.x
  // return [a.acceleration.x,a.acceleration.y,a.acceleration.z,a.gyro.x,a.gyro.y,a.gyro.z];
  // double data[6] = {a.acceleration.x, a.acceleration.y, a.acceleration.z, a.gyro.x, a.gyro.y, a.gyro.z};
}

double* getFilteredData(int n){
  double sums[6] = {0,0,0,0,0,0};

  static double avgs[6];

  //Finding sums
  for(int i=1; i<=n; i++){
    static double* data;
    data = getData();
    for(int j=0; j<6; j++){
      sums[j] = sums[j]+data[j];
    }
  }

  //Finding avgs
  for(int i=0; i<6; i++){
    avgs[i] = sums[i]/n;
  }

  return avgs;
}

double* calliberateSensor(){
  static double offsets[6];
  static double* data;
  data = getFilteredData(5);

  for(int i=0; i<6; i++){
    offsets[i] = data[i];
  }

  return offsets;
}

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
  //Initialize all pins
  for(int i=0;i<4;i++){
    pinMode(motor_pins[i],OUTPUT);
  }

  pinMode(LED_R_PIN,OUTPUT);
  pinMode(LED_G_PIN,OUTPUT);
  pinMode(LED_B_PIN,OUTPUT);
  pinMode(BUZZER_PIN,OUTPUT);

  pinMode(BTN_PIN,INPUT);

  //Initialize Serial
  SerialBT.begin(bt_name);
  Serial.begin(115200);
  delay(100);

  //Initialize MPU6050
  Wire.begin(SDA_PIN,SCL_PIN);
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  delay(100);

  //Calliberate sensor
  offsets = calliberateSensor();
}

void loop() {

  //Bluetooth read
  if(SerialBT.available()){
    char ch = SerialBT.read();
    if (ch == '\n') {
      stringEnd = true;
    } else {
      inputString += ch;
    }
  }
  if(stringEnd){
        inputString.trim();
        String* command = splitBySpace(inputString);

        //Update desired angles
        for(int i=0;i<3;i++){
          desiredAngles[i] = command[i].toDouble();
        }
        throttleIncrement = command[3].toDouble();

        inputString = "";
        stringEnd = false;
  }

  // Read Sensor data
    current_time = micros();
    data = getFilteredData(5);


    // Calculate angles
    dt = (current_time-previous_time)*pow(10,-6);
    //Integrated Angles
    for(int i=0;i<3;i++){
      integratedAngles[i]+=dt*(data[i+3]-offsets[i+3]);
    }

    //Angles from triginometry/Acceletration
    if(orientation == 2){
      if(data[0]==0){
        accAngles[1] = 3.14/2;
        accAngles[2] = 3.14/2;
      }else{
            accAngles[2] = atan(data[1]/data[0]);
            accAngles[1] = atan(data[2]/data[0]);
      }
    }
    //Sign correction
    if(orientation==2){
      // double temp=integratedAngles[0];
      accAngles[2] = -accAngles[2];
      // integratedAngles[0] = -temp;
    }
    // accAngles[0] = integratedAngles[0];
    // //Complementary filter
    for(int i=1; i<3; i++){
      currentAngles[i] = alpha*integratedAngles[i] + (1-alpha)*accAngles[i];
    }
    currentAngles[0] = integratedAngles[0];

    // PID control

    // Finding errors in angles
    for(int i =0;i<3;i++){
      current_errors[i] = currentAngles[i]-desiredAngles[i];
    }
    throttle+=throttleIncrement;
    throttleIncrement = 0;

    // // Find rate outputs:
    for(int i=0;i<3;i++){
      P_terms[i] = P*current_errors[i];
      I_terms[i] = I_terms[i]+I*current_errors[i]*dt;
      D_terms[i] = (current_errors[i]-previous_errors[i])/dt;

      // rate_outputs[i] = P_terms[i]+I_terms[i]+D_terms[i];
      rate_outputs[i] = P_terms[i];
    }
    //calculate motor inputs
    motor_inputs[0] = (throttle-rate_outputs[0]-rate_outputs[1]+rate_outputs[2])*255;
    motor_inputs[1] = (throttle-rate_outputs[0]+rate_outputs[1]-rate_outputs[2])*255;
    motor_inputs[2] = (throttle+rate_outputs[0]+rate_outputs[1]+rate_outputs[2])*255;
    motor_inputs[3] = (throttle+rate_outputs[0]-rate_outputs[1]-rate_outputs[2])*255;

    //Give motor inputs
    for(int i=0;i<4;i++){
      if(motor_inputs[i]<0){
        motor_inputs[i] = 0;
      }
      else if(motor_inputs[i]>255){
        motor_inputs[i] = 255;
      }
      Serial.print(motor_inputs[i]);
      Serial.print(" ");
    }
    Serial.println("");


    for(int i=0;i<3;i++){
      previous_errors[i] = current_errors[i];
    }
    previous_time = current_time;
}
