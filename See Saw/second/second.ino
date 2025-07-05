String inputString = "";
bool stringEnd = false;

String* splitBySpace(String str){
  static String words[10];int i=0;String word = "";int wordIndex = 0;
  while(i<str.length()){
    if((str[i]==' ')){
      words[wordIndex] = word;
      word="";
      wordIndex++;i++;
      continue;
    }
    if(i==str.length()-1){
      word+=str[i];
      words[wordIndex] = word;break;
    }
    word+=str[i];
    i++;
  }
  return words;
}

void setup() {
  Serial.begin(9600);
  delay(200);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
}

void loop() {
  if(stringEnd){
    inputString.trim();
    String* command = splitBySpace(inputString);
    analogWrite(9,command[0].toInt());
    analogWrite(10,command[1].toInt());

    Serial.println("M1, M2 = "+command[0]+", "+command[1]);

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
