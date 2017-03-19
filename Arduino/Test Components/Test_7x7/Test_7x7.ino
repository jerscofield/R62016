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

const uint8_t ledSpot[] = {14, 6, 5, 4, 3, 2, 1, 0, 14, 13, 12, 11, 10, 9, 8, 22, 21, 20, 19, 18, 17, 16, 30, 29, 28, 27, 26, 25, 24, 38, 37, 36, 35, 34, 33, 32, 46, 45, 44, 43, 42, 41, 40, 54, 53, 52, 51, 50, 49, 48, 55};

  int spot = 0;
  
int convertStr2Int(char digit);
void ledValues();

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
  char 
  
  char front;
  char right;
  char left;
 
        
        
  //   for (int i = 1; i < 50; i++)
   //     leds[ledSpot[i]] = CRGB::Blue;
    // FastLED.show();
  // digitalWrite(led_pin, led_state);    
  //look for serial from the pi
  //get the values from the sensors
  //send the values to the raspberry pi (determine beforehand where you are on the track -- are you on a tunnel edge?)
  //update the 7x7 LED display
  
  //wait until Pi is ready to communicate
  if (Serial.available() > 0){
  char number = Serial.read();
     
  switch(number){
    case 'a':  Serial.print("coo' coo'!");
               break;
    case 'b': ledValues();
              break;
    case 'c': 
    default:
              Serial.write('z');
       //put numbers on grids case 'c': put numbers on grids
  }
  }
  Serial.flush();
}


void ledValues()
{
  Serial.print("Now within the loop!");
  int number;
  String strNumber;
  char gridSpot;
  
  while (!Serial.available()){}

  //get grid
  strNumber = Serial.readString();
 
  number = 10*convertStr2Int(strNumber[0]) + convertStr2Int(strNumber[1]);
  gridSpot = strNumber[2];

        
        

  switch (gridSpot){
    case 'r':
        leds[ledSpot[number]] = CRGB::Red;
        break;
    case 'b':
        leds[ledSpot[number]] = CRGB::Blue;
        break;
    case 'g':
        leds[ledSpot[number]] = CRGB::Green;
        break;
    case 'p':
        leds[ledSpot[number]] = CRGB::Purple;
        break;
    case 'y':
        leds[ledSpot[number]] = CRGB::Yellow;        
        break;
    default:
        //Serial.print("Error: No Color Input");
        break;
  }
    FastLED.show();
    return;
                                                   
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
  return digitAsInt;

}


