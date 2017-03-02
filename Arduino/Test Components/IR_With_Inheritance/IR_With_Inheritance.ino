#include "IR.h"

#define ir A0

IR irSensor(ir);


void setup(){
  delay(3000);
  Serial.begin(9600)

}


void loop(){
  int dis = irSensor.getDistance();
  Serial.print(dis);
  Serial.print('\n');
  delay(200);


}



