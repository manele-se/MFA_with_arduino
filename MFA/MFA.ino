
#include <SoftwareSerial.h>
#define ID 0x5b
#define packetReceived  (protocolData[index] == ID && protocolData[(index+2)%3]== (protocolData[(index+1)%3] ^ ID))

SoftwareSerial bt(2,3); // RX, TX


 static int protocolData[3];
 static byte index = 0;
 static char done = 0;

 
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

void readOneByte(){

  if (bt.available() ) {
     done= 0; 
     char oneByte= bt.read(); 
     protocolData[index] = oneByte;
     index++;
     index = index %3; //circular buffer, avoiding buffer overflow
  }
}


// the loop function runs over and over again forever
void loop() {
  //read the bytes available and then fill in the bytes array.
  readOneByte(); 
  if (packetReceived){
      if (done == 0) {
        
        char id = protocolData[index]; 
        char code = protocolData[(index+1)%3];
        if(code)delay(3500);
         //empty buffer
        for(int i = 0; i< 3; i++){
        protocolData[i]=0;
       }
        blink_binary(code);
        int newCode = false; 
           
        }
    }
  }
