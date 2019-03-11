int IR_Sensor = A0;
int IR_LED = 4;
int x,y,z;
void setup() {
    Serial.begin(9600);
    pinMode(IR_Sensor, INPUT);
    pinMode(IR_LED, OUTPUT);

}

void loop() {
    digitalWrite(IR_LED, HIGH);
    //delay(1);
    x = analogRead(IR_Sensor);
    /*
    digitalWrite(IR_LED, LOW);
    delay(1);
    y = analogRead(IR_Sensor);

    z = x-y;
*/
    Serial.print(x);
    /*Serial.print("\t");
    Serial.print(y);
    Serial.print("\t");
    Serial.print(z);*/
    Serial.println();
}
