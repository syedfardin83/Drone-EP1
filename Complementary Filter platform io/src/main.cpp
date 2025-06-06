#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <math.h>


Adafruit_MPU6050 mpu;
double* offsets;
double* data;

int motor_pins[4] = {9,5,6,3};

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
  data = getData();

  for(int i=0; i<6; i++){
    offsets[i] = data[i];
  }

  return offsets;
}

double getRateFromAcc(int axis){
  double rate;
  if(axis==1){
    rate = atan(data[0]/data[2]);
  }
  return rate;
}

void setup(void) {

  // Reading mpu6050
  Serial.begin(115200);
  while (!Serial) {
    delay(10); // will pause Zero, Leonardo, etc until serial console opens
  }
  // Try to initialize!
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

  Serial.println("Calibertaing sensors. Make sure drone is at rest.");
  offsets = calliberateSensor();

  //Setup Motors
  pinMode(motor_pins[0],OUTPUT);
  pinMode(motor_pins[1],OUTPUT);
  pinMode(motor_pins[2],OUTPUT);
  pinMode(motor_pins[3],OUTPUT);
}

  //motor input
double throttle = 0.2;
double desired_rates[3] = {0,0,0};
double rate_inputs[3] = {0,0,0};
int motor_inputs[4] = {0,0,0,0};

double current_errors[3] = {0,0,0};
double prev_errors[3] = {0,0,0};

//time variables
unsigned long previous_time = 0;
unsigned long current_time = 0;
double dt;

//PID constants:
double P=0.08;
double I=0.01;
double D=0.01;

//PID terms:
double P_terms[3] = {0,0,0};
double I_terms[3] = {0,0,0};
double D_terms[3] = {0,0,0};

void loop() {
  previous_time = micros();
  //Update data
  data = getFilteredData(5);

  current_time = micros(); 
  dt = (current_time-previous_time)*pow(10,-6);

  // find current errors:
  for(int i=0;i<3;i++){
    current_errors[i] = data[i+3]-offsets[i+3]-desired_rates[i];
  }

  //Find rate inputs:
  for(int i=0;i<3;i++){
    P_terms[i] = P*current_errors[i];
    I_terms[i] = I_terms[i]+I*current_errors[i]*dt;
    D_terms[i] = (current_errors[i]-prev_errors[i])/dt;

    rate_inputs[i] = -(P_terms[i]+I_terms[i]);
  }

  //Calculate motor inputs:
  motor_inputs[0] = (throttle-rate_inputs[0]+rate_inputs[1]+rate_inputs[2])*255;
  motor_inputs[1] = (throttle-rate_inputs[0]-rate_inputs[1]-rate_inputs[2])*255;
  motor_inputs[2] = (throttle+rate_inputs[0]-rate_inputs[1]+rate_inputs[2])*255;
  motor_inputs[3] = (throttle+rate_inputs[0]+rate_inputs[1]-rate_inputs[2])*255;

  Serial.println(motor_inputs[0]);

  //Send motor signals
  // for(int i=0;i<4;i++){
  //   if(motor_pins[i]<=0){
  //     analogWrite(motor_pins[i],0);
  //   }
  //   analogWrite(motor_pins[i],motor_inputs[i]);
  // }

  //assign prev errors:
  for(int i=0;i<3;i++){
    prev_errors[i] = current_errors[i];
  }

  delay(10);
}





