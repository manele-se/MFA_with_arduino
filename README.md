# Specifications 

## Arduino board
Arduino Uno 

## Bluetooth shield
HM-10 Wireless Shield for Arduino Uno with Texas Instruments® CC2541 Bluetooth v4.0 BLE chip.

## Components
* 4 LEDs
* 4 resistors 220 ohm
* breadboard

# Goal 
This project creates a multi factor authentication solution using an Arduino board and a python server. 
The user data are saved in a database (which is a file). The password is hashed using SHA256. When the user logs in with the right credentials, a code in binary form is displayed on the LEDs on the Arduino board. The user needs to read the binary code and put the right decimal code on the application to get access to the Secret Bank. (ex. if the LEDs display 0011 the user needs to write 3 on the user interface).

It is possible to use this project as starting point to create a MFA which displays the code on a LED display instead of just 4 LEDS or other solution. 


## Software
Arduino IDE 
Python3 


# Procedure
* Install the shiled onto Arduino borad
* connect the jumpers on the HM10 shield 
* ground the board, ground each LED
* add 1 resistor to each LED 
* connect pins 4,5,6,7 to LEDS via resistors
* compile and upload the Arduino sketch

# Picture

![arduino.jpg](arduino.jpg | width= 300)