int IR_Sensor_Whisk1 = A0;
int IR_Sensor_Whisk2 = A1;
int IR_Sensor_Val1, IR_Sensor_Val2;

int Left_Enable = 2;
int Left_Forwards = 3;
int Left_Reverse = 5;
int Right_Enable = 4;
int Right_Forwards = 6;
int Right_Reverse = 9;

unsigned long previousMillis = 0;
unsigned long currentMillis = 0;
const long interval = 100;
String receivedData;
bool startFlag = 1;

void setup() {
  Serial.begin(9600);              //Starting serial communication
  pinMode(IR_Sensor_Whisk1, INPUT);
  pinMode(IR_Sensor_Whisk2, INPUT);

  pinMode(Left_Forwards, OUTPUT);
  pinMode(Left_Reverse, OUTPUT);
  pinMode(Right_Forwards, OUTPUT);
  pinMode(Right_Reverse, OUTPUT);
  pinMode(Left_Enable, OUTPUT);
  pinMode(Right_Enable, OUTPUT);
  digitalWrite(Left_Enable, HIGH);
  digitalWrite(Right_Enable, HIGH);
}

void loop() {
  // Wait to receive instruction from Pi before doing anything else
  // Do as instruction says (Go forwards, left etc.)
  // Start reading and sending data from sensors to PI at specified time intervals.
  // This will determine sample rate of collected data. Use millis() for this.
  
  while (startFlag == 1) {
    if (Serial.available() > 0) {
      startFlag = 0;
    }
    // Waiting to receive data from Pi
  }
  currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    sendData();
  }
  recData();
}

void sendData() {
  IR_Sensor_Val1 = analogRead(IR_Sensor_Whisk1);
  IR_Sensor_Val2 = analogRead(IR_Sensor_Whisk2);
  Serial.print(IR_Sensor_Val1);
  Serial.print(',');
  Serial.print(IR_Sensor_Val2);
  Serial.print('\n');
}

void recData() {
  if (Serial.available() > 0) {
    receivedData = Serial.readString();
    Serial.print(receivedData);
    if (receivedData == "Forward") {
      forwards();
    }
    else if(receivedData == "Reverse") {
      reverse();
    }
    else if(receivedData == "Left") {
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
void forwards() {
  analogWrite(Left_Forwards, 255);
  analogWrite(Right_Forwards, 255);
  analogWrite(Left_Reverse, 0);
  analogWrite(Right_Reverse, 0);
}
void reverse() {
  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Reverse, 255);
  analogWrite(Right_Reverse, 255);
}
void turnLeft() {
  analogWrite(Left_Forwards, 255);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Reverse, 0);
  analogWrite(Right_Reverse, 255);
}
void turnRight() {
  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 255);
  analogWrite(Left_Reverse, 255);
  analogWrite(Right_Reverse, 0);
}
void stopRobot() {
  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Reverse, 0);
  analogWrite(Right_Reverse, 0);
}
