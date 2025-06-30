String inputString = "";
bool stringComplete = false;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

void loop() {
  if (stringComplete) {
    inputString.trim(); // Remove unwanted \r or spaces

    if (inputString == "TURN_ON_LED") {
      digitalWrite(13, HIGH);
      Serial.println("Turned on LED");
    } else if (inputString == "TURN_OFF_LED") {
      digitalWrite(13, LOW);
      Serial.println("Turned off LED");
    }

    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char ch = (char)Serial.read();
    if (ch == '\n') {
      stringComplete = true;
    } else {
      inputString += ch;
    }
  }
}
