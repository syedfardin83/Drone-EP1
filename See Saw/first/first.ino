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
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  // analogWrite(9,0);
}

void loop() {
  // put your main code here, to run repeatedly:
  // if(stringEnd){
  //   inputString.trim();
    
  //   Serial.println(inputString);

  //   inputString = "";
  //   stringEnd = false;
  // }
  Serial.println("HEy");
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
