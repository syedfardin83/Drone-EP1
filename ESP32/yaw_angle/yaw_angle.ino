#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <math.h>

Adafruit_MPU6050 mpu;

// Motor pins
int motor_pins[4] = {12,13,14,27};

// Sensor orientation
#define orientation 2

// MPU6050 pins
#define SCL_PIN 26
#define SDA_PIN 25


// Drone control variables
double desiredAngles[3] = {0,0,0};
int desiredThrottle = 0.2;
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
double P=0.1,I=0.01,D=0.01;
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

void setup() {
  //Initialize Serial
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
  // Read Sensor data
  current_time = micros();
  data = getFilteredData(5);


  // Calculate angles
  dt = (current_time-previous_time)*pow(10,-6);
  //Integrated Angles
  
  integratedAngles[0]+=dt*(data[3]-offsets[3]);
  Serial.println(degrees(integratedAngles[0]));
  


  previous_time = current_time;
}
