
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
  static int protocolData[3];
  static byte index = 0;
  static char done = 0;  
  //read the bytes available and then fill in the bytes array.
  if (bt.available() ) {
     done= 0; 
     char oneByte= bt.read(); 
     protocolData[index] = oneByte;
     index++;
     index = index %3; //circular buffer
    }

  
    if (protocolData[index] == ID && protocolData[(index+2)%3]== (protocolData[(index+1)%3] ^ ID)){
      if (done == 0) {
      
        char id = protocolData[index]; 
        char code = protocolData[(index+1)%3];
        delay(3000);
        blink_binary(code);
        delay(3000);
        blink_binary(0);
        done=1; 
        //empty buffer
        for(int i = 0; i< 3; i++){
        protocolData[i]=0;
       }
        
       
        }
    }
  }
