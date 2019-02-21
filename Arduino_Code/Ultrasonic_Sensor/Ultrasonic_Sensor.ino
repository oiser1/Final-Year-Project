int trigPin = 8;    //Trigger (PWM Pin)
int echoPin = 7;    //Echo
float pulseDelay, objectDistance;

void setup() {
    Serial.begin(9600);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}
// the loop function runs over and over again forever
void loop() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);

    pulseDelay = pulseIn(echoPin, HIGH);

    objectDistance = ((pulseDelay/2)*0.000343);

    Serial.print(objectDistance);
    Serial.print("metres");
    Serial.println();
    delay(1000);
}
