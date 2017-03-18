#include <SharpIR.h>
#include <Arduino.h>


/* PIN definitions */
// built in LED
const byte led_pin = LED_BUILTIN;  
 // Button on pin-2, internal pullup
const byte but_pin = 3;           
// the number of the pushbutton pin
const int buttonPin = 2;     
int buttonState = 0;

/* Volatile variables modified in the ISR */
volatile boolean led_state = LOW;
volatile unsigned int last_but_ptime = 0;

byte number = 0;
int state = 0;

//IR Sensor
#define ir A0
#define ir2 A1
#define ir3 A2
//#define ir A2
#define model 20150
//boolean done=false;
SharpIR sharp1(ir, 25, 93, model);
SharpIR sharp2(ir2, 25, 93, model);
SharpIR sharp3(ir3, 25, 93, model);


boolean isEMF();
boolean ObjInFront();
boolean ObjOnLeft();
boolean ObjOnRight();


void setup()
{
  Serial.begin(9600);
  //tester LED
  pinMode(13, OUTPUT); 
  pinMode(led_pin, OUTPUT);
  pinMode(but_pin, INPUT_PULLUP);
  pinMode (ir, INPUT);
}

/* Show the led_state on the internal LED, it is changed in the ISR */
void loop()
{
  // digitalWrite(led_pin, led_state);    
    
  //look for serial from the pi
  //get the values from the sensors
  //send the values to the raspberry pi (determine beforehand where you are on the track -- are you on a tunnel edge?)
  //update the 7x7 LED display
  
  //wait until Pi is ready to communicate
  while(Serial.available() == 0){}

   number = Serial.read();
   
   
   switch(number):{
     case 'a': // getCapacitance();
                front = objInFront();
                Serial.write(front);
                break;
     case 'b': right = objOnRight();
               front = objInFront();
               left = objOnLeft();
               Serial.write(right);
               Serial.write(front);
               Serial.write(left);
               break;
     //put numbers on grids case 'c': put numbers on grids
}


//determine if there is an EMF signal under the robot. might change this function to color light sensor
boolean isEMF(){
  //if on EMF tunnel, 
  //return true;
  //else
  //return false;
  return true;
}

//checks for obstacle in front of the robot
//I think that this sensor only detects within 10 t0 80 CM
//should be able to check 3 blocks
char objInFront(){
  int dis = sharp1.distance();
  
  if(dis > 75)
    return '0';  //there is no obstacle in front of sensor
   else 
     return '1';  //there is an obstacle in front of sensor
}

////checks for obstacle in front of the robot
char objOnLeft(){
  int dis = sharp2.distance();
  
  if(dis > 75)
    return '0';  //there is no obstacle in front of sensor
   else 
     return '1';  //there is an obstacle in front of sensor
}

//checks for obstacle in front of the robot
char objOnRight(){
  int dis = sharp3.distance();
  
  if(dis > 75)
    return '0';  //there is no obstacle in front of sensor
   else 
     return '1';  //there is an obstacle in front of sensor
}




