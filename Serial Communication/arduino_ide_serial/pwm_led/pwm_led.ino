String inputString = "";
bool stringEnd = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(9,OUTPUT);
  analogWrite(9,0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(stringEnd){
    inputString.trim();
    int pwmValue = inputString.toInt();
    analogWrite(9,pwmValue);
    Serial.println("PWM set to "+inputString);

    inputString = "";
    stringEnd = false;
  }
}

void serialEvent(){
  while(Serial.available()){
    char ch = Serial.read();
    if (ch == '\n') {
      stringEnd = true;
    } else {
      inputString += ch;
    }
  }
}
