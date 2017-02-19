//temp char to send
int sendMe = 3;


#include <SharpIR.h>
//IR Sensor
#define ir A0
#define model 20150
//boolean done=false;
SharpIR sharp(ir, 25, 93, model);




void setup(){
Serial.begin(9600);
  pinMode (ir, INPUT);


}


void loop(){

  int dis = sharp.distance();
  //send ASCII char to PI
  
  //go straight
  if(dis > 100)
    Serial.println(0);   //nothing here, go straight
  else
    Serial.println(1);  //something here, turn
  
//  Serial.println(sendMe);
  delay(100);
}
