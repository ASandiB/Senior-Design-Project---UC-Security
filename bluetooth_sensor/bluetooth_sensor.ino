// These files belong to the 2025 Winter Senior Design Project
// UC Security - Ryan Suarez, Anthony Sandi, Giovanni Guiliana
// This code was written and implemented by Anthony Sandi

#include <SPI.h>
#include <BluetoothSerial.h>
#include <esp_bt_device.h>
#include <nRF24L01.h>
#include <RF24.h>

const int DOOR_SENSOR_PIN = 15; // Arduino pin connected to door sensor's pin
const int motionSensor = 13; // Arduino pin connected to PIR sensor

int currentDoorState; 
int lastDoorState;
String receivedData = "";
int motionDetected;

BluetoothSerial SerialBT;

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! please run 'make menuconfig' to and enable it
#endif

// nRF24L01+ transmission modules setup
RF24 radio(4,5);
const byte address[6] = "00001";

// How to get the ESP32 Bluetooth address for Raspberry Pi connection
void printDeviceAddress(){
  const uint8_t* point = esp_bt_dev_get_address();

  for(int i=0; i<6; i++){
    char str[3];
    sprintf(str, "%02X", (int)point[i]);
    Serial.print(str);

    if(i<5){
      Serial.print(":");
    }
  }
}

// Setting up modules for radio connection and bluetooth
void setup() {
  Serial.begin(9600);
  pinMode(DOOR_SENSOR_PIN, INPUT_PULLUP);
  pinMode(motionSensor, INPUT_PULLUP);
  Serial.println("\n---Start---");
  SerialBT.begin("ESP32test");
  Serial.println("BT MAC: ");
  printDeviceAddress();
  Serial.println();
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}

void loop() {
  doorlockstate = LOW;
  lastDoorState = currentDoorState;              
  currentDoorState  = digitalRead(DOOR_SENSOR_PIN);
  const char text[] = "Unlock the Door!";
  motionDetected = digitalRead(motionSensor);
  // Recieving Bluetooth Data from Raspberry Pi
  if (SerialBT.available()) {
      receivedData = SerialBT.readStringUntil('\n'); 
      Serial.print("Received from Pi: ");
      Serial.println(receivedData);
  }
  // Sending door sensor information back to the Raspberry Pi
  if (lastDoorState == LOW && currentDoorState == HIGH) { 
    Serial.println("The door-opening event is detected");
    SerialBT.println("Door Opened!");
    delay(500);
  }
  else if (lastDoorState == HIGH && currentDoorState == LOW) { 
    Serial.println("The door-closing event is detected");
    SerialBT.println("Door Closed!");
  }
  // Sending other ESP32 requests to open door if recieved data from Raspberry Pi was a recognition
  if (receivedData == "Familiar Face!"){
    radio.write(&text, sizeof(text));
    Serial.println("I recognize them!");
  }
  // Telling the camera to wake up for power reduction
  if(motionDetected == 1){
    SerialBT.println("Someone's Here!");
    Serial.println("Someone's Here!");
  }
  receivedData = "";
}
