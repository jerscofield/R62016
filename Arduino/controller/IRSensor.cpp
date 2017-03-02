#define ir A0


#include "IRSensor.h" //include the declaration for this class
 
//const byte BUTTON_PIN = 2; //use the LED @ Arduino pin 13, this should not change so make it const (constant)
 
//<<constructor>> setup the LED, make pin 13 an OUTPUT
IRSensor::IRSensor(int irPin){
  //  this->pin = BUTTON_PIN;
    _pin = irPin
    SharpIR sharp(ir, 25, 93, model);
	//isDown = true;
}


float IRSensor::getDistance(){
	int reading = analogRead(_pin);
	return reading;
}
 
//<<destructor>>
IRSensor::~IRSensor(){/*nothing to destruct*/}
 

//tests to see if object is in front of robot



