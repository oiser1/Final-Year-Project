char dataString[50] = {0};
int a =0; 
char receivedData;
String entireMessage;

void setup() {
Serial.begin(9600);              //Starting serial communication
}
  
void loop() {
  /*
  a++;                          // a value increase every loop 
  Serial.println(a);            // send the value a over serial
  delay(1000);                  // pause for 1 second
  */

  /* If there is data in the serial buffer, reads data and appends it to string.
      Else tells Pi it is not working */
  if (Serial.available() > 0) {
    receivedData = Serial.read();
    entireMessage += receivedData;
  }
  else {
    Serial.println("not working");
  }
  Serial.println(entireMessage);  // Sends string to serial TX and back to Pi
  delay(1000);
}
