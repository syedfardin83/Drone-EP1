#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <math.h>


Adafruit_MPU6050 mpu;
double* offsets;
double* data;
double z = 0;

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
  if(axis==2){
    rate = atan(data[2]/data[0]);
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
  Wire.begin(25,26);
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
}

unsigned long previous_time = 0;
unsigned long current_time = 0;
double dt;

void loop() {
  current_time = micros();
  //Update data
  data = getFilteredData(5);
   
  dt = (current_time-previous_time)*pow(10,-6);

  z+=dt*(data[3]-offsets[3]);
  

  double accAngle = getRateFromAcc(2);
  // Serial.println(degrees(accAngle));
  double angle = -0.98*z+0.02*z;
  Serial.print(degrees(accAngle));
  Serial.print("  ");
  Serial.print(degrees(z));
  previous_time = current_time;
  delay(10);
  Serial.println("");
}





