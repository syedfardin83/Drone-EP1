#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

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

  int pm1 = 9;
  int pm2 = 5;
  int pm3 = 6;
  int pm4 = 3;

  pinMode(pm1,OUTPUT);
  pinMode(pm2,OUTPUT);
  pinMode(pm3,OUTPUT);
  pinMode(pm4,OUTPUT);

  int des_r = 0;
  int des_p = 0;
  int des_y = 0;
}

void loop() {

  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  // AccX = a.acceleration.x
  delay(10);


}