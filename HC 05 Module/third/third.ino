#include <SoftwareSerial.h>

SoftwareSerial BTSerial(2, 3); // RX, TX (Arduino reads on 2, writes on 3)

void setup() {
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  Serial.begin(9600);     // For Serial Monitor (optional)
  BTSerial.begin(9600);   // HC-05 default baud rate

  Serial.println("Bluetooth ready!");
  BTSerial.println("Hello from Arduino!");
}

void loop() {
  if (BTSerial.available()) {
    char data = BTSerial.read();
    Serial.print("Received: ");
    Serial.println(data);

    // Respond or control stuff based on command
    if (data == '1') {
      digitalWrite(13,HIGH);
      // digitalWrite(motorPin, HIGH); etc
    }
    if (data == '0') {
      digitalWrite(13,LOW);
      // digitalWrite(motorPin, HIGH); etc
    }
  }

  // You can send data to phone too:
  // BTSerial.println("Arduino says hi");
}
