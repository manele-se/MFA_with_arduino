
#include <SoftwareSerial.h>
#define ID 0x5b

SoftwareSerial bt(2,3); // RX, TX

int 

// the setup function runs once when you press reset or power the board
void setup() {
  bt.begin(9600);
  pinMode(7, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);  

  blink_binary(0);
}

void blink_binary(int value){

  for(int i = 0 ; i<4; i++){
    if(value & (1 << i)) 
        digitalWrite(7-i, HIGH); 
    else 
         digitalWrite(7-i, LOW); 
  }
}

// the loop function runs over and over again forever
void loop() {
  static int bytes[3];
  //read the bytes available and then complete the bytes array.
  if (bt.available()) {
    bytes[2]= bt.read(); //crc
    bytes[1]= bt.read(); //code
    bytes[0]= bt.read();//id 
      
    if (bytes[0] == ID && (ID ^ bytes[2]) == crc){
       delay(3000);
       blink_binary(code);
       delay(3000);
       blink_binary(0);
    }
  }else if (bt.available()) {
    bt.read();

  
   
  }
}
