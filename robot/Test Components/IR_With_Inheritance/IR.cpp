#include "IR.h"//include the declaration for this class
 
//const byte BUTTON_PIN = 2; //use the LED @ Arduino pin 13, this should not change so make it const (constant)
IR::IR(){

    this->pin = A0;
    pinMode(pin, INPUT); //make that pin an input
    sharp(pin,25,93,20150);
}


//<<constructor>> setup the IR sensor
IR::IR(int BUTTON_PIN){

    this->pin = BUTTON_PIN;
    pinMode(pin, INPUT); //make that pin an input
    sharp(pin,25,93,20150);
}

 
//<<destructor>>
IR::~IR(){/*nothing to destruct*/
     ~sharp;
}
 


//turn the LED on
int IR::getDistance(void){
     sharp.setDistance();
     return sharp.distance();
}

void IR::setDistance(void){
     this->distance = sharp.distance();
     return;
}









//how do I do pinmode in here?
//is ir an integer or a string?
