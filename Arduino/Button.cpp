#include "Button.h" //include the declaration for this class
 
//const byte BUTTON_PIN = 2; //use the LED @ Arduino pin 13, this should not change so make it const (constant)
 
//<<constructor>> setup the LED, make pin 13 an OUTPUT
Button::Button(int BUTTON_PIN){
    this->pin = BUTTON_PIN;
    pinMode(pin, INPUT); //make that pin an input
	//isDown = true;
}
 
//<<destructor>>
Button::~Button(){/*nothing to destruct*/}
 


//turn the LED on
bool Button::isDown(void){
  	int val1 = digitalRead(pin);  // read input value

        if(val1 == LOW)
		return false;
	else if (val1 == HIGH)
		return true;
}

