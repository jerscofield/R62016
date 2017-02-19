//#include "LED13.h"
#include <FastLED.h>


//8x8 matrix
#define LED_PIN     5
#define NUM_LEDS    64
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];
#define UPDATES_PER_SECOND 100
CRGBPalette16 currentPalette;
TBlendType    currentBlending;
extern CRGBPalette16 myRedWhiteBluePalette;
extern const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM;

char grid[63];

void setup() {
  delay(3000);
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps

  ///8x8 display
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    
    //fill grid pattern with *'s temporarily
    for(int i = 0; i < NUM_LEDS; i++)
    {
      grid[i] = '*';
    }
    
    //temporary grid pattern
    grid[0] = 's';
    grid[13] = 'd';
    grid[26] = 'd';
    grid[52] = 'd';
    grid[17] = 'd';    
    grid[22] = 'm';    
    grid[23] = 'm';
    grid[24] = 'm';
    grid[25] = 'm';
}

void loop(){
    
        static uint8_t startIndex = 0;
        startIndex = startIndex + 1; /* motion speed */
    
       //Fill 8x8 grid with colors
        fillGrid(startIndex);
        
        //display values
        FastLED.show();
     //   FastLED.delay(1000 / UPDATES_PER_SECOND);

}


//fill the grid with colors based on array values
void fillGrid( uint8_t colorIndex)
{
    uint8_t brightness = 255;

    
    for( int i = 0; i < NUM_LEDS; i++) {
      
       // delay(100);
         char blockType = grid[i];
         Serial.print(blockType);
     
         switch(blockType){
             //start corner
             case 's':
                  leds[i] = CRGB::Yellow;
                  Serial.print("working");
                  break;
             //deadend
             case 'd':
                  leds[i] = CRGB::Blue;
                  break;
             //mapped grid location
             case 'm':
                  leds[i] = CRGB::Red;
                  break;
             default:
                  leds[i] = CRGB::White;       
       }
            // leds[i] = CRGB::Yellow;
    }
  }
