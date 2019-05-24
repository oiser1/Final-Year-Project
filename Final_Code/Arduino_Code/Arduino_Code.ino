// Code written by Oisin Walsh as part of a bachelor thesis in TU Dublin. 
// Last edit made 24/05/2019
// Some of the code in this program was taken from the following link and modified
// to suit the purposes of this program: https://www.arduino.cc/reference/en/

// Analog input pins are initialised with relevant names of type int
int IR_Sensor_LeftWhisk = A0;
int IR_Sensor_RightWhisk = A1;
int IR_Sensor_Left, IR_Sensor_Right; // set as type int

// Digital output pins are initialised with relevant names of type int
int Right_Enable = 2;
int Right_Reverse = 3;
int Right_Forwards = 5;
int Left_Enable = 4;
int Left_Reverse = 6;
int Left_Forwards = 9;

// Variables created to be used in millis functionality.
unsigned long previousMillis = 0;
unsigned long currentMillis = 0;
const long interval = 10; // Period between samples in milliseconds

// string which will hold message received from Pi. And start flag
// initialised to 1.
String receivedData;
bool startFlag = 1;

// Setup section of Arduino code
void setup() {
  // Starting serial communnication at baud rate of 2 million. Same as on the
  // Raspberry Pi its communicating with.
  Serial.begin(2000000);
  
  // Pins set as inputs connected to IR sensor to read in data from it
  pinMode(IR_Sensor_LeftWhisk, INPUT);
  pinMode(IR_Sensor_RightWhisk, INPUT);

  // Pins set as outputs for control of motors. Pins are connected to the driver
  // chip, including the enable pins for the driver chip which are also set 
  // HIGH here.
  pinMode(Left_Forwards, OUTPUT);
  pinMode(Left_Reverse, OUTPUT);
  pinMode(Right_Forwards, OUTPUT);
  pinMode(Right_Reverse, OUTPUT);
  pinMode(Left_Enable, OUTPUT);
  pinMode(Right_Enable, OUTPUT);
  digitalWrite(Left_Enable, HIGH);
  digitalWrite(Right_Enable, HIGH);
}

// Start of main loop of Arduino code
void loop() {
  // Wait to receive instruction from Pi before doing anything else
  // Do as instruction says (Go forwards, left etc.)
  // Start reading and sending data from sensors to PI at specified time intervals.
  // This will determine sample rate of collected data. Use millis() for this.

  // Arduino will be stuck in this while loop until it receives data in the serial
  // pins which is connected to the Raspberry Pi.
  while (startFlag == 1) {
    if (Serial.available() > 0) {
      startFlag = 0; // Once data is received from Pi, flag is set to false
    }
    // Waiting to receive data from Pi
  }

  // 'millis()' tracks time since program started. The program is required to take
  // a sample from the IR sensor every 10ms, so if the current 'millis()' time is 
  // more than or equal to 10ms, the program will send sensor data to the Pi. 
  // previous 'millis()' is set as current 'millis()' and the program continues.
  currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    sendData(); // calls function to send IR sensor data to Pi
  }
  recData(); // calls to read from serial pins and do what message says
}

// 'sendData()' function. Reads from pins connected to IR sensors and
// sends to Pi. Will be an 'int' and range from 0-1023. Each piece of data
// is followed with sending '\n' which seperates each piece of data from another.
void sendData() {
  IR_Sensor_Left = analogRead(IR_Sensor_LeftWhisk);
  IR_Sensor_Right = analogRead(IR_Sensor_RightWhisk);
  Serial.print(IR_Sensor_Left);
  Serial.print('\n');
  Serial.print(IR_Sensor_Right);
  Serial.print('\n');
}

// 'recData()' function. If there's no data in the serial buffer, function will jump 
// to end. If there is data, its read in as a string and saved in 'receivedData'.
void recData() {
  if (Serial.available() > 0) {
    receivedData = Serial.readString();
    // If  the received message is any of the following strings it will call the 
    // relevant function
    if (receivedData == "Forward") {
      forwards();
    }
    else if (receivedData == "Reverse") {
      reverse();
    }
    else if (receivedData == "Left") {
      turnLeft();
    }
    else if (receivedData == "Right") {
      turnRight();
    }
    else if (receivedData == "Stop") {
      stopRobot();
    }
    else {
      // Change nothing
    }
  }
}
// Following are robot direction and control functions. They are on PWM (Pulse Width 
// Modulation) pins so power can be set from 0-255 (0-5 volts). Because the right motor
// is a little more powerful than the left, which orginally left the robot slowly
// drifting, the power was set lower on the pins for the right motor to go forwards
// and reverse.
void forwards() {
  analogWrite(Left_Forwards, 255);
  analogWrite(Right_Forwards, 242);
  analogWrite(Left_Reverse, 0);
  analogWrite(Right_Reverse, 0);
}
void reverse() {
  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Reverse, 255);
  analogWrite(Right_Reverse, 242);
}
void turnLeft() {
  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 242);
  analogWrite(Left_Reverse, 255);
  analogWrite(Right_Reverse, 0);
}
void turnRight() {
  analogWrite(Left_Forwards, 255);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Reverse, 0);
  analogWrite(Right_Reverse, 242);
}
void stopRobot() {
  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Reverse, 0);
  analogWrite(Right_Reverse, 0);
}
