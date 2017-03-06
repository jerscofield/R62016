#include "IRSensor.h"

#define ir A0

IRSensor irsensor = IRSensor();


void setup() {
  delay(3000);
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  pinMode (ir, INPUT);
}

void loop(){
  
  
}



