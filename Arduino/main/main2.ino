#include <SharpIR.h>

/* Interrupt on a button
 * By: Jeffrey Hundstad <we0a@arrl.net> 2015-03-09
 * Documentation on AttachInterrupt:
 *  http://arduino.cc/en/Reference/AttachInterrupt 


/* PIN definitions */
const byte led_pin = LED_BUILTIN;  // built in LED
const byte but_pin = 3;            // Button on pin-2, internal pullup
const int buttonPin = 2;     // the number of the pushbutton pin
int buttonState = 0;

/* Volatile variables modified in the ISR */
volatile boolean led_state = LOW;
volatile unsigned int last_but_ptime = 0;

byte number = 0;
int state = 0;

//IR Sensor
#define ir A0
#define model 20150
//boolean done=false;
SharpIR sharp(ir, 25, 93, model);


/*
button press code:
1 - start button has been pressed
*/

void setup()
{
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
  pinMode(led_pin, OUTPUT);
  pinMode(but_pin, INPUT_PULLUP);
  pinMode (ir, INPUT);

  /*
   * attachInterrupt(interrupt, ISR, mode)
   *  interrupt = [0 == pin 2, 1 == pin 3]
   *  MODE = [LOW, CHANGE, RISING, FALLING]
   */
  attachInterrupt(1, blink, RISING);
  
  
  //wait for the button to be pressed (we still need to buy an inverted schmitt trigger)
  while (buttonState != HIGH) {
    //  Serial.write("can't start car until button is pressed!");
      buttonState = digitalRead(buttonPin);
  }
  Serial.write('1');
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
  while(!Serial.available());

   number = Serial.read();
   if (number == 'd')
     Serial.write('z');
   //Serial.write(number);
 //  Serial.print("character recieved");
  // Serial.print(number);
//   if (number != 'd')
  //   while(1);
   //get and send values to the pi
   boolean emf_values = isEMF();
   boolean obj_in_front = objInFront();
   
   if(isEMF())
     Serial.write('E');
   else
     Serial.write('F');
     
   if(objInFront())
     Serial.write('G');
   else
     Serial.write('H');
     
   //Serial.write(emf_values);
   //Serial.write(obj_in_front);
   
   //update the 7x7 grid
 
   digitalWrite(led_pin, led_state);
}


/* Intended to be attached as an ISR */
/* Change the led_state but on as fast as PRESS_DELAY */
const unsigned int PRESS_DELAY = 100; /* milliseconds */
void blink()
{
  unsigned int but_ptime = millis();
  if ( (but_ptime - last_but_ptime) > PRESS_DELAY) {
    last_but_ptime = but_ptime;
    led_state = !led_state;
  }
}

//determine if there is an EMF signal under the robot
boolean isEMF(){
  //if on EMF tunnel, 
  //return true;
  //else
  //return false;
  return true;
}

boolean objInFront(){
  int dis = sharp.distance();
  
  if(dis > 100)
    return true;
   else 
     return false;
}

