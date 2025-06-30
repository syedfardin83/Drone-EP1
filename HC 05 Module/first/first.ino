char data;

void setup() {
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  Serial.begin(38400);
  pinMode(8, OUTPUT);
}

void loop() {
  if (Serial.available()>0) {
    data = Serial.read();
    // if (data == '1') {
    //   digitalWrite(8, HIGH);
    // } else if (data == '0') {
    //   digitalWrite(8, LOW);
    // }
    Serial.println(data);
    if(data=='1'){
      digitalWrite(13,HIGH);
    }
    if(data=='0'){
      digitalWrite(13,LOW);
    }
  }
}
