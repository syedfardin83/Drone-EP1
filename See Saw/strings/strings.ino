// const int MAX_WORDS = 10;

// String* splitBySpace(String input) {
//   static String words[MAX_WORDS];  // Static so it persists after return
//   int index = 0;

//   input.trim();  // Remove leading/trailing spaces

//   while (index < MAX_WORDS && input.length() > 0) {
//     int spaceIndex = input.indexOf(' ');

//     if (spaceIndex == -1) {
//       words[index++] = input;
//       break;
//     }

//     words[index++] = input.substring(0, spaceIndex);
//     input = input.substring(spaceIndex + 1);
//     input.trim();  // Remove extra spaces at start
//   }

//   return words;
// }

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
  delay(100);
  // put your setup code here, to run once:
  String sentence = "Hello Arduino World";
  String* words = splitBySpace(sentence);
  
  Serial.print(words[0]);
}

void loop() {
  // put your main code here, to run repeatedly:

}
