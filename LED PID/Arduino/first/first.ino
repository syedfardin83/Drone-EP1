void setup() {
  // put your setup code here, to run once:
  pinMode(9,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(3,OUTPUT);
  int delay = 50;


}

void loop() {
  // put your main code here, to run repeatedly:
  // digitalWrite(9,HIGH);
  // digitalWrite(5,HIGH);
  // digitalWrite(6,HIGH);
  // digitalWrite(3,HIGH);


    digitalWrite(9,LOW);
  digitalWrite(5,LOW);
  digitalWrite(6,LOW);
  digitalWrite(3,LOW);

  delay(delay);
  digitalWrite(9,HIGH);
  delay(delay);
  digitalWrite(9,LOW);
delay(delay);
  digitalWrite(5,HIGH);
  delay(delay);
  digitalWrite(5,LOW);
  delay(delay);
  digitalWrite(6,HIGH);
  delay(delay);
  digitalWrite(6,LOW);
  delay(delay);
  digitalWrite(3,HIGH);
  delay(delay);
  digitalWrite(3,LOW);
}
