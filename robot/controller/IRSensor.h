#include <SharpIR.h>

#ifndef IRSensor_H
#define IRSensor_H
 
#include <Arduino.h>
#include <SharpIR.h>
 
class IRSensor public SharpIR{
public:
        IRSensor(int irPin);

        float getDistance();
        ~IRSensor();
	//void write7seg();
	bool objectInFront;
private:
	//int pin;
};
 
#endif
