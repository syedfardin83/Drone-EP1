//LOS 2.0 - FreeRTOS Based 6dof, bluetooth controlled Lark Firmware
//Three main tasks
//1. Bluetooth Input
//2. MPU6050 Sensor input and processing
//3. PID

//  Axis mapping:
//  x-axis : yaw
//  y-axis : pitch
//  z-axis : roll 

//ToDO:
//vTaskDelay after every task
//Proper heap memory allocation for each task

//  Importing modules
#include "BluetoothSerial.h"
#include <math.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

//  Defining App CPU  
#if CONFIG_FREERTOS_UNICORE
static const int app_cpu = 0;
#else
static const int app_cpu = 1;
#endif

//  Software Objects
BluetoothSerial SerialBT;
Adafruit_MPU6050 mpu;

//  BT read variables
String inputString = "";
bool stringEnd = false;
char ch;

// Drone control variables
double desiredAngles[3] = {0,0,0}; ////////////////////////////
double throttleIncrement = 0;
double throttle = 0; //////////////////
double* offsets;
double integratedAngles[3] = {0,0,0};
double accAngles[3] = {0,0,0};
double compAngles[3] = {0,0,0};
double alpha = 0.98;

//MPU
#define SCL_PIN 17
#define SDA_PIN 26
double* mpu_data;////////////////////////////

// PID variables
double P=0.09,I=0.01,D=0.01;
double P_terms[3] = {0,0,0};
double I_terms[3] = {0,0,0};
double D_terms[3] = {0,0,0};
double current_errors[3] = {0,0,0};
double previous_errors[3] = {0,0,0};
double rate_outputs[3] = {0,0,0};

// Motor inputs
int motor_inputs[4] = {0,0,0,0};

// Time variables
double dt1;

#define bt_name "LOS 2.0"

//  FreeRTOS Queues
static QueueHandle_t desiredAnglesQ;
static uint8_t desiredAnglesQ_l = 3;

static QueueHandle_t throttleQ;
static uint8_t throttleQ_l = 3;

static QueueHandle_t mpu_dataQ;
static uint8_t mpu_dataQ_l = 3;

static QueueHandle_t dt1Q;
static uint8_t dt1Q_l = 3;

static QueueHandle_t current_anglesQ;
static uint8_t current_anglesQ_l = 3;


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

//  FreeRTOS Tasks
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
      throttle+=(throttleIncrement*0.1);
      throttleIncrement = 0;

      //  Push to queue
      if(xQueueSend(desiredAnglesQ, desiredAngles,3) != pdTRUE){
        Serial.println("desiredAnglesQ full!");
      }

      if(xQueueSend(throttleQ, &throttle, 3) != pdTRUE){
        Serial.println("throttle Q full!");
      }

      inputString = "";
      stringEnd = false;
    }
    vTaskDelay(10/portTICK_PERIOD_MS);
  }
}

void mpu_read_pid_task(void *param){
  Serial.println("Entered MPU task");
  static TickType_t last_tick;
  static TickType_t curr_tick;
  int i;

  while(1){
    // prev_tick = xTaskGetTickCount();
    last_tick = xTaskGetTickCount();
    mpu_data = getFilteredData(5);
    curr_tick = xTaskGetTickCount();

    dt1 = ((curr_tick-last_tick)*portTICK_PERIOD_MS)/1000;
    
    //  Push To Queue
    if(xQueueSend(mpu_dataQ, mpu_data, 3) != pdTRUE){
      Serial.println("mpu_dataQ full!");
    }

    if(xQueueSend(dt1Q, &dt1, 3) != pdTRUE){
      Serial.println("dt1Q full!");
    }

    vTaskDelayUntil(&last_tick, 40/portTICK_PERIOD_MS);
  }
}

void calculate_angles_task(void *param){
  double dt1; double mpu_data_local[6];int i;
  while(1){
    //  Read Queues
    if(xQueueReceive(dt1Q,&dt1,3)!=pdTRUE){
      Serial.println("Failed to read dt1Q");
    }
    
    if(xQueueReceive(mpu_dataQ,&mpu_data_local,3) != pdTRUE){
      Serial.println("Failed to read mpu_dataQ");
    }

    //  Integrate Angles
    for(i=0;i<3;i++){
      integratedAngles[i]+=dt1*(mpu_data_local[i+3]-offsets[i+3]);
    }

    //  Acc angles
    accAngles[0] = -integratedAngles[0];
    if(mpu_data[0]==0){
      accAngles[1] = 3.14/2;
      accAngles[2] = 3.14/2;     
    }else{
      accAngles[1] = atan(mpu_data_local[2]/mpu_data_local[0]);
      accAngles[2] = atan(mpu_data_local[1]/mpu_data_local[0]);
    }

    //  Complementary filter
    for(i=0;i<3;i++){
      compAngles[i] = alpha*integratedAngles[i] + (1-alpha)*accAngles[i];
    }

    //  Update Queue
    if(xQueueSend(current_anglesQ,&compAngles,3)!=pdTRUE){
      Serial.println("current_anglesQ full!");
    }
  }
}

void pid_task(void *param){
  double current_angles[3]; double desired_angles_loacal[3]; double throttle_local;
  static TickType_t last_tick;
  static TickType_t curr_tick;
  double dt2;
  while(1){
    //  Read Queues
    if(xQueueReceive(current_anglesQ,&current_angles,3)!=pdTRUE){
      Serial.println("Failed to read current_anglesQ");
    }

    if(xQueueReceive(desiredAnglesQ,&desired_angles_loacal,3)!=pdTRUE){
      Serial.println("Failed to read desiredAnglesQ");
    }

    if(xQueueReceive(throttleQ,&throttle_local,3)!=pdTRUE){
      Serial.println("Failed to read throttleQ");
    }

    //Find errors
    prev_tick = xTaskGetTickCount();
    for(i=0;i<3;i++){
      current_errors[i] = current_angles[i]-desired_angles_loacal[i];
    }
    curr_tick = xTaskGetTickCount();
    dt2 = ((curr_tick-last_tick)*portTICK_PERIOD_MS)/1000;


    //Find rate outputs
    //****************** dt not properly calculated *****************************
    for(i=0;i<3;i++){
      P_terms[i] = P*current_errors[i];
      I_terms[i] = I_terms[i]+I*current_errors[i]*dt2;
      D_terms[i] = (current_errors[i]-previous_errors[i])/dt2;

      rate_outputs[i] = P_terms[i];
    }
    
    motor_inputs[0] = (throttle_local+rate_outputs[1]-rate_outputs[2]+rate_outputs[0])*255;
    motor_inputs[1] = (throttle_local+rate_outputs[1]+rate_outputs[2]-rate_outputs[0])*255;
    motor_inputs[2] = (throttle_local-rate_outputs[1]+rate_outputs[2]+rate_outputs[0])*255;
    motor_inputs[3] = (throttle_local-rate_outputs[1]-rate_outputs[2]-rate_outputs[0])*255;

    // **************** Give motor inputs - waiting ****************************
  }
}

void setup() {
  SerialBT.begin(bt_name);
  Serial.begin(115200);
  delay(100);

  //  Intitialize FreeRTOS Queues
  desiredAnglesQ = xQueueCreate(desiredAnglesQ_l, sizeof(double)*3);
  throttleQ = xQueueCreate(throttleQ_l, sizeof(double));
  mpu_dataQ = xQueueCreate(mpu_dataQ_l, sizeof(double)*6);
  dt1Q = xQueueCreate(dt1Q_l, sizeof(double));
  current_anglesQ = xQueueCreate(current_anglesQ_l, sizeof(double)*3);

  //  Initialize MPU6050
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

    //Create and run MPU task
  xTaskCreatePinnedToCore(
    mpu_read_pid_task,
    "mpu_read_pid_task",
    2048,
    NULL,
    1,
    NULL,
    app_cpu
  );
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
  //Create and run Calculate Angles task
  xTaskCreatePinnedToCore(
    calculate_angles_task,
    "Calculate Angles",
    2048,
    NULL,
    2,
    NULL,
    app_cpu
  );
  //Create and run PID task
  xTaskCreatePinnedToCore(
    pid_task,
    "PID",
    2048,
    NULL,
    2,
    NULL,
    app_cpu
  );

}

void loop() {
}
