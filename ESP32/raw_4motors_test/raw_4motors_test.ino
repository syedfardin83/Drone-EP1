void setup() {
  // put your setup code here, to run once:
  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
  pinMode(14,OUTPUT);
  pinMode(27,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(12,HIGH);
  analogWrite(13,100);
  digitalWrite(14,HIGH);
  digitalWrite(27,HIGH);
}
