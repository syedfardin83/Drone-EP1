void setup() {
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  Serial.begin(9600); // Start serial at 9600 baud
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    // Serial.print("Echo: ");
    if(c=='1'){
      digitalWrite(13,HIGH);
      Serial.println("LED turned on!");
    }else if(c=='0'){
      digitalWrite(13,LOW);
      Serial.println("LED turned off!");
    }else{
      Serial.println("Unknown Command.");
    }
  }
}