void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    String mensagem = Serial.readString();
    String str;
    
    for(int i=0; i< mensagem.length(); i++){
      char c = mensagem.charAt(i);  
      for(int i=7; i>=0; i--){
        str += bitRead(c,i);
      }
    }
    
//    Serial.println(str);
    
    int ruido = random(0,str.length());
//    Serial.println(ruido);
//    Serial.println(str.charAt(ruido));

    if(str.charAt(ruido) == '1'){
      str.setCharAt(ruido, '0');
    }else{
      str.setCharAt(ruido, '1');
    }

    
    Serial.println(str);
  }
}
