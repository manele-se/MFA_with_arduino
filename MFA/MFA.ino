
#include <SoftwareSerial.h>
#define ID 0x5b

SoftwareSerial bt(2,3); // RX, TX

// the setup function runs once when you press reset or power the board
void setup() {
  bt.begin(9600);
  pinMode(7, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);  

  blink_binary(14);
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
  if (bt.available()== 3) {
    int id = bt.read();
    int code = bt.read();
    int crc = bt.read();

    if (id == ID && (ID ^ code) == crc){
       delay(3000);
       blink_binary(code);
       delay(3000);
       blink_binary(0);
    }
   
  }
}
