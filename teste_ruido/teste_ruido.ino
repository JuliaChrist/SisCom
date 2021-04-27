void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  String mensagem = Serial.readString();
  String str = "";
  
  for(int i=0; i< mensagem.length(); i++){
      char c = mensagem.charAt(i);  
      for(int i=7; i>=0; i--){
          str += bitRead(c,i);
      }
  }
  
  Serial.print(str);
  Serial.println("");
  delay(2000);





  
}
