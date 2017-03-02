#include "BUTTONS.h"

const int ledPin1 = 12; // choose the pin for the LED
const int ledPin2 = 13; // choose the pin for the LED
const int inPin1 = 2;   // choose the input pin (for a pushbutton)
const int inPin2 = 3;   // choose the input pin (for a pushbutton)
int val1 = 0;     // variable for reading the pin status
int val2 = 0;     // variable for reading the pin status


//constructor
BUTTONS::BUTTONS(){}


BUTTONS::BUTTONS(){
  pinMode(ledPin1, OUTPUT);  // declare LED as output
  pinMode(ledPin2, OUTPUT);  // declare LED as output
  pinMode(inPin1, INPUT);    // declare pushbutton as input
  pinMode(inPin2, INPUT);    // declare pushbutton as input
}


//destructor
BUTTONS::~BUTTONS(){}

void BUTTONS::respond2Button(){
  val1 = digitalRead(inPin1);  // read input value
  val2 = digitalRead(inPin2);  // read input value

  if (val1 == LOW) {         // check if the input is HIGH (button released)
    digitalWrite(ledPin1, LOW);  // turn LED OFF
  } else {
    digitalWrite(ledPin1, HIGH);  // turn LED ON
  }
  
  if (val2 == LOW) {         // check if the input is HIGH (button released)
    digitalWrite(ledPin2, LOW);  // turn LED OFF
  } else {
    digitalWrite(ledPin2, HIGH);  // turn LED ON
  }
  return;
}
