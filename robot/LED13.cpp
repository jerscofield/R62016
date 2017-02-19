#include "LED13.h" //include the declaration for this class
 
//const byte LED_PIN = 13; //use the LED @ Arduino pin 13, this should not change so make it const (constant)
 
//<<constructor>> setup the LED, make pin 13 an OUTPUT
LED13::LED13(int LED_PIN){
    this->pin = LED_PIN;
    pinMode(pin, OUTPUT); //make that pin an OUTPUT
}
 
//<<destructor>>
LED13::~LED13(){/*nothing to destruct*/}
 
//turn the LED on
void LED13::on(){
        digitalWrite(pin,HIGH); //set the pin HIGH and thus turn LED on
}
 
//turn the LED off
void LED13::off(){
        digitalWrite(pin,LOW); //set the pin LOW and thus turn LED off
}
 
//blink the LED in a period equal to paramterer -time.
void LED13::blink(int time){
        on();                   //turn LED on
        delay(time/2);  //wait half of the wanted period
        off();                  //turn LED off
        delay(time/2);  //wait the last half of the wanted period
}
