#ifndef Button2_H
#define Button2_H
 
#include <Arduino.h>
 
class Button2 {
public:
        Button2(int BUTTON_PIN);
        ~Button2();
	//bool isDown;
	bool isDown();
private:
	int _pin;
};
 
#endif
