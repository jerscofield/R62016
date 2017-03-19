#include <FastLED.h>
#include <Arduino.h>

#define LED_PIN     7
#define NUM_LEDS    55
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB

#define kMatrixWidth 8
#define kMatrixHeight 8

#define UPDATES_PER_SECOND 100
CRGB leds[kMatrixWidth * kMatrixHeight];


CRGBPalette16 currentPalette;
TBlendType    currentBlending;

extern CRGBPalette16 myRedWhiteBluePalette;
extern const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM;

const uint8_t ledSpot[] = {0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54};
int convertStr2Int(char digit);

void setup() {
    Serial.begin(9600);
    delay( 3000 ); // power-up safety delay
//    LEDS.addLeds<SMART_MATRIX>(leds,NUM_LEDS);
  //  LEDS.setBrightness(96);
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
    FastLED.setBrightness(  96 );
        fill_solid( currentPalette, 16, CRGB::White);
    
}


void loop()
{
  
  char front;
  char right;
  char left;
  int number1Int;
  int number2Int;
  int number;
  
  char gridType;
  char number1;
  char number2;
  // digitalWrite(led_pin, led_state);    
  //look for serial from the pi
  //get the values from the sensors
  //send the values to the raspberry pi (determine beforehand where you are on the track -- are you on a tunnel edge?)
  //update the 7x7 LED display
  
  //wait until Pi is ready to communicate
  if (Serial.available() > 0){
  char data2Get = Serial.read();
     
  switch(data2Get){
    case 'a':  Serial.print("coo' coo'!");
               break;
    case 'b': 
              break;
    case 'c': number1 = Serial.read();
              number2 = Serial.read();
              gridType = Serial.read();
              
              number1Int = convertStr2Int(number1);
              number2Int = convertStr2Int(number2);
              number = 10*number1Int + number2Int;
                                                        
              switch(gridType){
                if (gridType == 'r')
                  leds[ledSpot[number]] = CRGB::Red;
                else if (gridType == 'b')
                  leds[ledSpot[number]] = CRGB::Blue;
                else if (gridType == 'g')
                  leds[ledSpot[number]] = CRGB::Green;
                else if (gridType == 'y')
                  leds[ledSpot[number]] = CRGB::Yellow;
                else if (gridType == 'p')
                  leds[ledSpot[number]] = CRGB::Purple;                  
              }                                                        

              FastLED.show();
              break;
    default:
              Serial.write('z');
       //put numbers on grids case 'c': put numbers on grids
  }
}



int convertStr2Int(char digit){
  int digitAsInt = 0;
  
  switch(digit){
    case'0':
      digitAsInt = 0;
      break;
    case'1':
      digitAsInt = 1;
      break;
    case'2':
      digitAsInt = 2;
      break;
    case'3':
      digitAsInt = 3;
      break;
    case'4':
      digitAsInt = 4;
      break;
    case'5':
      digitAsInt = 5;
      break;
    case'6':
      digitAsInt = 6;
      break;
    case'7':
      digitAsInt = 7;
      break;
    case'8':
      digitAsInt = 8;
      break;
    case'9':
      digitAsInt = 9;
      break;  
    default:
      digitAsInt = 0;    
        
  }

}
