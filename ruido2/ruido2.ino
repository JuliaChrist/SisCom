void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

/*Transforma uma mensagem em uma string contendo seu valor binário*/
//TA OK, NÃO MEXER
String ASCII_to_Binary(String str){
  String str_bin;
  for (int i = 0; i < str.length(); i++){
    char c = str.charAt(i);  
    for (int j = 7; j >= 0; j--){
      str_bin += bitRead(c,j);
    }
  }
  return (str_bin);
}

/*Converte a string em binário em um vetor do tipo int*/
//TA OK, NÃO MEXER
void String_to_Int_List(String str, int *int_list){
  for (int i = 0; i < str.length(); i++){
    if(str[i] == '1'){
      int_list[i] = 1;
    }else{
      int_list[i] = 0;
    }
//    Serial.print(int_list[i]);
  }
//  Serial.println("");
}

/*INsere o ruído no sinal*/
//TA OK, NÃO MEXER
String Insert_Noise(String str){
  int noise = random(0,str.length());
    if(str.charAt(noise) == '1'){
      str.setCharAt(noise, '0');
    }else{
      str.setCharAt(noise, '1');
    }
    return (str);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){

    String mensagem = Serial.readString();

    String str;
    str = ASCII_to_Binary(mensagem);
    int n_bytes = (str.length())/8;
//    Serial.println(n_bytes);
//    str = Insert_Noise(str);
//    Serial.println(str);

    /*Separa a string de 8 em 8 bits em um vetor de strings. Cada elemento do vetor contém a string com o valor binário do respectivo byte*/
    int count = 0;
    String str_split[n_bytes];
    
    for (int i = 0; i < str.length(); i += 8){
      for (int j = i; j < i+8; j++){
        str_split[count] += str[j];
      }
//      Serial.print(str_split[count]);
      count++;
//      Serial.println("");
    }

  //converter cada string em um vetor de int, converter cada vetor em seu valor decimal 
    int int_mat[n_bytes][8], dec_values[n_bytes];
    String str_return;
    
    for (int i = 0; i < n_bytes; i++){
      String_to_Int_List(str_split[i],int_mat[i]);
      dec_values[i] = 0;
      int _exp = 1;
      
      //começar pelo bit menos significativo
      for (int j = 7; j >= 0; j--){
         dec_values[i] += int_mat[i][j] * _exp;
         _exp = _exp * 2;
      }
//      Serial.println(dec_values[i]);
      str_return += char(dec_values[i]);
    }


    Serial.println(str_return);
  }
}
