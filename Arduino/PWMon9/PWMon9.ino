void setup() {
  // put your setup code here, to run once:
  pinMode(9,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(9,0);
  for(int i=0;i<20;i++){
    delay(200);
    analogWrite(9,i*10);
  }
  for(int j=20;j>=1;j--){
    delay(200);
    analogWrite(9,j*10);
  }
  // digitalWrite(9,HIGH);
}
