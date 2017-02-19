#include <SharpIR.h>




//IR Sensor
#define ir A0
#define model 20150
//boolean done=false;
SharpIR sharp(ir, 25, 93, model);



void setup() {
  delay(3000);
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
//  button1 = button(2);
  pinMode (ir, INPUT);
}




void loop(){
  
  //if button is pressed -- start (need button variable)
  
  


  int dis = sharp.distance();
  Serial.print(dis);
  Serial.print('\n');
  
  
  delay(200);
    //turn left  
    //threshold is 100 ... for now
    

}


/*
void getIRDistance(){
 delay(100);    // it gives you time to open the serial monitor after you upload the sketch

// if (done==false){  // it only runs the loop once
 
 for(int i = 0; i < 10; i++){
  unsigned long pepe1=millis();  // takes the time before the loop on the library begins
  int dis=sharp.distance();  // this returns the distance to the object you're measuring
  Serial.print("Mean distance: ");  // returns it to the serial monitor
  Serial.println(dis);
  unsigned long pepe2=millis()-pepe1;  // the following gives you the time taken to get the measurement

  Serial.print("Time taken (ms): ");
  Serial.println(pepe2);  
  delay(100);
 }
 
 
//done=true;

 //}
 return;

}
*/



