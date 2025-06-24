void setup() {
  Serial.begin(9600); // Start serial at 9600 baud
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); // Read until newline
    Serial.print("Arduino Received: ");
    Serial.println(data); // Echo back to Python (optional)
  }
}