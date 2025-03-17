// These files belong to the 2025 Winter Senior Design Project
// UC Security - Ryan Suarez, Anthony Sandi, Giovanni Guiliana
// This code was written and implemented by Anthony Sandi

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <ESP32Servo.h>

// nRF24L01+ transmission modules setup
RF24 radio(4,5);
const byte address[6] = "00001";

// Servo and variables setup
Servo myservo;
int servoPin = 12;
int pos = 0;
unsigned long previousMillis = 0;
unsigned long servoMovement = 15;
unsigned long doorDelay = 10000;
unsigned long lastMoveTime = 0; 
bool movingBack = false;
bool commandReceived = false;
String lastRecieved = "Bad";

// Setting up modules for radio connection and servo communication
void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0,address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  myservo.setPeriodHertz(50); 
  myservo.attach(servoPin, 500, 2400);
}

void loop() {
  // If information is available from the transciever, then to unlock the door
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));
    Serial.println(text);

    // Ensure there are no extra whitespaces
    String receivedText = String(text);
    receivedText.trim();  

    if (receivedText == "Unlock the Door!") {
      lastRecieved = "Good";
      Serial.println("Unlock the Door command received");
    }
  }
  if(lastRecieved == "Good"){
      moveServoToUnlock(); // Moves the servo based on this flag
  }

}
// Servo movement while keeping in mind the no use of delay() as it would jam our system
void moveServoToUnlock() {
  unsigned long currentMillis = millis();  

  if (!movingBack && pos <= 63) {
    if (currentMillis - previousMillis >= servoMovement) {
      previousMillis = currentMillis; 
      myservo.write(pos);  
      Serial.print("Moving to position: "); // A bit of debugging code
      Serial.println(pos);
      pos++;  
    }
  }

  
  if (pos == 63 && lastMoveTime == 0 && !movingBack) {
    lastMoveTime = currentMillis;  
    movingBack = true;  
    Serial.println("Reached position 65, waiting for 10 seconds"); // A bit of debugging code
  }


  if (movingBack && currentMillis - lastMoveTime >= doorDelay) {
    if (pos > 0) {
      myservo.write(pos);  
      Serial.print("Moving back to position: "); // A bit of debugging code
      Serial.println(pos);
      pos--;  
    }
  }


  if (pos == 0 && movingBack) {
    Serial.println("Servo has returned to position 0"); // A bit of debugging code
    // Resetting flags for next movement
    movingBack = false;
    lastMoveTime = 0;  
    pos = 0;
    
    lastRecieved = "Bad"; // Resets this flag
  }
}
