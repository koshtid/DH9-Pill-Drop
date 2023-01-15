
/*
  For DeltaHacks and the Drug Dealing Pill Dispenser 2023
  Dhanya Koshti
  Leanne Chen
  Zara Khan

  Connects to Raspberry Pi via I2C - Arduino slave & Pi Master
  Operates servo motors
  Uses capacitive touch sensor to check if there's any pills in the compartment left
  
*/
 
// Include the Wire library for I2C
#include <Wire.h>
// Include the Servo lib
#include <Servo.h>

// Servo Coding
Servo s1;
Servo s2;
Servo s3;
int pos1 = 0;
int pos2 = 0;
int pos3 = 0;

// // Touch Sensor Coding
const int touchSensor = 2; //touch sensor to arduino pin 2
int touchState = 0; //read sensor status

// //Buzzer Coding
const int buzzer = 3; //sets buzzer to pin 3
int pillRemind = 0; //flag variable buzzer, pill taking reminder

void dispensePill(Servo myservo, int &pos){
  
  if (pos == 0){
    myservo.write(180);
    pos = 180;              // tell servo to go to position in variable 'pos'
    delay(1000);                       // waits 15ms for the servo to reach the position
  }  
  
  else if(pos != 0){
    myservo.write(0);
    pos = 0;              // tell servo to go to position in variable 'pos'
    delay(1000);                       // waits 15ms for the servo to reach the position
  }
}

void setup() {
  // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  Serial.begin(9600);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveData);

  // Setup for Servo
  s1.attach(11);
  s2.attach(10);
  s3.attach(9);

  //Setup for touchsensor, buzzer 
  pinMode(touchSensor, INPUT);
  pinMode(buzzer, OUTPUT); // Set buzzer - pin 3 as an output
}

void receiveData(int byteCount) {
  while (Wire.available()) { // loop through all but the last
    int c = Wire.read(); // receive byte as a character
    Serial.print('\n');

    switch (c) {
      case 1:
        dispensePill(s1, pos1);
        Serial.print(pos1, '\n');
        break;
      case 2:
        dispensePill(s2, pos2);
        Serial.print(pos2, '\n');
        break;
      case 3:
        dispensePill(s3, pos3);
        Serial.print(pos3, '\n');
        break;
      case 4:
        pillRemind = 1; //changes flag variable for when you need to take your pills!!
        break;
      
    }
  }
}

void loop() {

  int counter = 0;

  touchState = digitalRead(touchSensor);
  
  if (touchState == HIGH){ // this means YOU NEED TO REFILL !
    tone(buzzer, 1000); // Send 1KHz sound signal...
    delay(1000);        // ...for 1 sec
    noTone(buzzer);     // Stop sound...
    delay(1000);        // ...for 1sec    
  }

  if (pillRemind == 1){
    tone(buzzer, 2000); // Send 2KHz sound signal...
    delay(2000);        // ...for 2 sec
    noTone(buzzer);     // Stop sound...
    delay(1000);        // ...for 1sec
    tone(buzzer, 2000); // Send 2KHz sound signal...
    delay(2000);        // ...for 2 sec
    noTone(buzzer);     // Stop sound...
    delay(1000);        // ...for 1sec

    pillRemind = 0;
  }  
}

