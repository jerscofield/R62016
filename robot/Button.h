#ifndef Button_H
#define Button_H
 
#include <Arduino.h>
 
class Button {
public:
        Button(int BUTTON_PIN);
        ~Button();
	//bool isDown;
	bool isDown();
private:
	int pin;
};
 
#endif
