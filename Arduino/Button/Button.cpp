#include "Button.h" //include the declaration for this class

//const byte BUTTON_PIN = 2; //use the LED @ Arduino pin 13, this should not change so make it const (constant)
 
//<<constructor>> setup the LED, make pin 13 an OUTPUT
Button::Button(int BUTTON_PIN){
    this->_pin = BUTTON_PIN;
    pinMode(BUTTON_PIN, INPUT); //make that pin an input
	//isDown = true;
}
 
//<<destructor>>
Button::~Button(){/*nothing to destruct*/}
 


//turn the LED on
void Button::isDown(void){
  	/*int val1 = digitalRead(pin);  // read input value

        if(val1 == HIGH)
		Serial.write('1');
	else
		Serial.write('2');*/

	Serial.write('g');
}

