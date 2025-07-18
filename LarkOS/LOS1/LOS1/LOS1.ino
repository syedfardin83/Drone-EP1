//Lark Operating System - 1
// Only one degree of freedom (throttle control only)
// Main tasks:
// 1. Test Button
// 2. Take bluetooth input
// 3. Take sensor input
// 4. PID loop
// 5. Indicators - LED/Buzzer.

//Test Button
#define TEST_BTN_PIN NULL

//Motor pins
#define M1_PIN NULL
#define M2_PIN NULL
#define M3_PIN NULL
#define M4_PIN NULL

//Sensor Pins
#define SDA_PIN NULL
#define SCL_PIN NULL

//Indicator pins
#define LED_R_PIN NULL
#define LED_G_PIN NULL
#define LED_B_PIN NULL
#define BUZZ_PIN NULL

void setup() {
  //Initialize all pins
  pinMode(TEST_BTN_PIN,INPUT);

  pinMode(M1_PIN, OUTPUT);
  pinMode(M2_PIN, OUTPUT);
  pinMode(M3_PIN, OUTPUT);
  pinMode(M4_PIN, OUTPUT);
  

  pinMode(LED_R_PIN, OUTPUT);
  pinMode(LED_G_PIN, OUTPUT);
  pinMode(LED_B_PIN, OUTPUT);
  pinMode(BUZZ_PIN,OUTPUT);

  //Initialize Serial
  Serial.begin(115200);
}

void loop() {

  //All components check protocol
  if(digitalRead(TEST_BTN_PIN == HIGH)){
    checkProtocol();
  }

  

}
