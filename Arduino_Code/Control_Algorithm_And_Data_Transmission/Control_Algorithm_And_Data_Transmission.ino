int IR_Sensor_Whisk1 = A0;
int IR_Sensor_Whisk2 = A1;
int IR_Sensor_Val1, IR_Sensor_Val2;

int IR_Sensor_FrontLeft = A3;
int IR_Sensor_FrontRight = A4;
int IR_Sensor_BackLeft = A5;
int IR_Sensor_BackRight = A6;

int trigPin = 11;    //Trigger
int echoPin = 12;    //Echo
float pulseDelay, objectDistance;

int Left_Enable = 2;
int Left_Forwards = 3;
int Left_Backwards = 5;
int Right_Enable = 4;
int Right_Forwards = 6;
int Right_Backwards = 9;

bool startFlag = true;

void setup() {
  Serial.begin(9600);              //Starting serial communication
  pinMode(IR_Sensor_Whisk1, INPUT);
  pinMode(IR_Sensor_Whisk2, INPUT);

  pinMode(IR_Sensor_FrontLeft, INPUT);
  pinMode(IR_Sensor_FrontRight, INPUT);
  pinMode(IR_Sensor_BackLeft, INPUT);
  pinMode(IR_Sensor_BackRight, INPUT);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(Left_Forwards, OUTPUT);
  pinMode(Left_Backwards, OUTPUT);
  pinMode(Right_Forwards, OUTPUT);
  pinMode(Right_Backwards, OUTPUT);
  pinMode(Left_Enable, OUTPUT);
  pinMode(Right_Enable, OUTPUT);
  digitalWrite(Left_Enable, HIGH);
  digitalWrite(Right_Enable, HIGH);

}

void loop() {
  // UART Code stuff
  IR_Sensor_Val1 = analogRead(IR_Sensor_Whisk1);
  Serial.print(IR_Sensor_Val1);
  Serial.print('\n');
  Serial.print(IR_Sensor_Val2);
  Serial.print('\n');
  //delay(1000);

  // Ultrasonic sensor code stuff
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  pulseDelay = pulseIn(echoPin, HIGH);
  objectDistance = ((pulseDelay/2)*0.000343);

  //Other IR sensors
  


  // Control algorithm
  if (startFlag) {
    turnRight();
    delay(3000);
    startFlag = false;
  }

  

}

void forwards() {
  analogWrite(Left_Forwards, 255);
  analogWrite(Right_Forwards, 255);
  analogWrite(Left_Backwards, 0);
  analogWrite(Right_Backwards, 0);
}
void backwards() {
  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Backwards, 255);
  analogWrite(Right_Backwards, 255);
}
void turnLeft() {
  analogWrite(Left_Forwards, 255);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Backwards, 0);
  analogWrite(Right_Backwards, 255);
}
void turnRight() {
  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 255);
  analogWrite(Left_Backwards, 255);
  analogWrite(Right_Backwards, 0);
}
void stopRobot() {
  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Backwards, 0);
  analogWrite(Right_Backwards, 0);
}
