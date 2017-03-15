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
//#define ir A2
#define model 20150
//boolean done=false;
SharpIR sharp(ir, 25, 93, model);
boolean ObjInFront();


void setup()
{
  Serial.begin(9600);
  //tester LED
  pinMode(13, OUTPUT); 
 // pinMode(buttonPin, INPUT);
  pinMode(led_pin, OUTPUT);
  pinMode(but_pin, INPUT_PULLUP);
  pinMode (ir, INPUT);

}

/* Show the led_state on the internal LED, it is changed in the ISR */
void loop()
{


  int dis = sharp.distance();
  Serial.print(dis);
  Serial.print('\n');
  delay(500);
  
}


//checks for obstacle in front of the robot
//I think that this sensor only detects within 1 foot
boolean objInFront(){
  int dis = sharp.distance();
  
  if(dis > 100)
    return true;
   else 
     return false;
}



