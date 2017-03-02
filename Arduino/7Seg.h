#ifndef 7Seg_H
#define 7Seg_H
 
#include <Arduino.h>
 
class 7Seg {
public:
        7Seg(int BUTTON_PIN);
        ~7Seg();
	void write7Seg();
private:
	int latchPin = 2;
	int dataPin = 3;
	int clockPin = 4;
};
 
#endif
