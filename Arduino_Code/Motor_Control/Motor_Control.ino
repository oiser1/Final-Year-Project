int Left_Enable = 2;
int Left_Forwards = 3;
int Left_Backwards = 5;
int Right_Enable = 4;
int Right_Forwards = 6;
int Right_Backwards = 9;
void setup() {
    // put your setup code here, to run once:
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
  // put your main code here, to run repeatedly:
  analogWrite(Left_Forwards, 255);
  analogWrite(Right_Forwards, 255);
  analogWrite(Left_Backwards, 0);
  analogWrite(Right_Backwards, 0);
  delay(3000);

  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Backwards, 255);
  analogWrite(Right_Backwards, 255);
  delay(3000);

  analogWrite(Left_Forwards, 255);
  analogWrite(Right_Forwards, 0);
  analogWrite(Left_Backwards, 255);
  analogWrite(Right_Backwards, 0);
  delay(3000);

  analogWrite(Left_Forwards, 0);
  analogWrite(Right_Forwards, 255);
  analogWrite(Left_Backwards, 255);
  analogWrite(Right_Backwards, 0);
  delay(3000);
  
}
