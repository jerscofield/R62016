
#ifndef IR_H
#define IR_H

#include <SharpIR.h>
#include <Arduino.h>
 
class IR : public SharpIR 
{
  public:
    IR();
    IR(int BUTTON_PIN);
    ~IR();
  	int getDistance();
  
  private:
  	int pin;
    int distance;
    void setDistance();
     SharpIR sharp;
};



 
#endif
