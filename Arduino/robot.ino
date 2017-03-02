#include "LED13.h"
#include "Button.h"
#include <SharpIR.h>
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


//IR Sensor
#define ir A0
#define model 20150
//boolean done=false;
SharpIR sharp(ir, 25, 93, model);


int incomingByte=0;
//BUTTONS button;


int ascii2dec(int);
LED13 led(12);
LED13 led2(13);
//Button button(2);
//Button button2(3);


//7 segment display
int latchPin = 2; // pin 12
int dataPin = 3; // pin 14
int clockPin = 4; // pin 11





void setup() {
  delay(3000);
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
//  button1 = button(2);
  pinMode (ir, INPUT);
  
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  
  
  
  ///8x8 display
      FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    
    currentPalette = RainbowColors_p;
    currentBlending = LINEARBLEND;


}




void loop(){
  //val1 = digitalRead(inPin1);  // read input value
  //val2 = digitalRead(inPin2);  // read input value
  
  int whichFunction;
  
  
 // bool state = button.isDown();
 // bool state2 = button2.isDown();
  
  /*
  if (state)
      led.on();
  else if (state2)
      led2.on();
  else{
      led.off();
      led2.off();
  }*/
    
    
  
  if (Serial.available() > 0) {
                // read the incoming byte:
                incomingByte = Serial.read();

                 //convert incoming byte from ascii to decimal
                whichFunction = ascii2dec(incomingByte);
                // say what you got:
   //             Serial.println(whichFunction, DEC);
    }
  
  
  //temp value to run motor from arduino
 //whichFunction = 6;


  
  //take input from serial monitor. decide which component to demonstrate
  switch (whichFunction) {
    case 0:    //get ir values
      for(;;){
           // getIRDistance();
            int dis = sharp.distance();
            Serial.print(dis);
            Serial.print('\n');
            delay(1000);
      }
      getIRDistance();
      break;
    case 1:    //get capacitive sensor values

      break;
    case 2:    //get EMF values

      break;
    case 3:    //cycle through LED matrix
      for(int k = 0; k < 25; k++){
        ChangePalettePeriodically();
    
        static uint8_t startIndex = 0;
        startIndex = startIndex + 1; /* motion speed */
    
        FillLEDsFromPaletteColors( startIndex);
    
        FastLED.show();
        FastLED.delay(1000 / UPDATES_PER_SECOND);
      }

      break;
    case 4:    //cycle through #'s on 7-segment LED display
     write7Seg();
      break;
    case 5:    //Take a picture

      break;
    case 6:    //Go straight
    Serial.println(6);   // send the data
 //   delay(1000);                  // give the loop some break
      break;
    case 7:    //Turn right
    Serial.println(7);   // send the data
    delay(1000);                  // give the loop some break
      break;
    case 8:    //Turn left
      Serial.println(8);   // send the data
      delay(1000);                  // give the loop some break
      break;
    case 9:    //Go backwards
      Serial.println(9);   // send the data
      delay(1000);                  // give the loop some break
      break;
    default: 
      // if nothing else matches, do the default
      // default is optional
    break;
  }  

}



int ascii2dec(int asciiVal){
  return (asciiVal - 48);
}



void write7Seg(){


    //1
  digitalWrite(latchPin, HIGH);
  shiftOut(dataPin, clockPin, MSBFIRST, 91);
  digitalWrite(latchPin, LOW);
  delay(1000);

    //2
  digitalWrite(latchPin, HIGH);
  shiftOut(dataPin, clockPin, MSBFIRST, 79);
  digitalWrite(latchPin, LOW);
  delay(1000);

    //3
  digitalWrite(latchPin, HIGH);
  shiftOut(dataPin, clockPin, MSBFIRST, 102);
  digitalWrite(latchPin, LOW);
  delay(1000);

    //4
  digitalWrite(latchPin, HIGH);
  shiftOut(dataPin, clockPin, MSBFIRST, 109);
  digitalWrite(latchPin, LOW);
  delay(1000);

    //5
  digitalWrite(latchPin, HIGH);
  shiftOut(dataPin, clockPin, MSBFIRST, 124);
  digitalWrite(latchPin, LOW);
  delay(1000);
  
      //6
  digitalWrite(latchPin, HIGH);
  shiftOut(dataPin, clockPin, MSBFIRST, 6);
  digitalWrite(latchPin, LOW);
  delay(1000);
  
  return;
}



void getIRDistance(){
 delay(100);    // it gives you time to open the serial monitor after you upload the sketch

// if (done==false){  // it only runs the loop once
 
 for(int i = 0; i < 10; i++){
  unsigned long pepe1=millis();  // takes the time before the loop on the library begins
  int dis=sharp.distance();  // this returns the distance to the object you're measuring
  Serial.print("Mean distance: ");  // returns it to the serial monitor
  Serial.println(dis);
  unsigned long pepe2=millis()-pepe1;  // the following gives you the time taken to get the measurement

  Serial.print("Time taken (ms): ");
  Serial.println(pepe2);  
  delay(100);
 }
//done=true;

 //}
 return;

}





//everything below is 8x8 display
void FillLEDsFromPaletteColors( uint8_t colorIndex)
{
    uint8_t brightness = 255;
    
    for( int i = 0; i < NUM_LEDS; i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        colorIndex += 3;
    }
}


// There are several different palettes of colors demonstrated here.
//
// FastLED provides several 'preset' palettes: RainbowColors_p, RainbowStripeColors_p,
// OceanColors_p, CloudColors_p, LavaColors_p, ForestColors_p, and PartyColors_p.
//
// Additionally, you can manually define your own color palettes, or you can write
// code that creates color palettes on the fly.  All are shown here.

void ChangePalettePeriodically()
{
    uint8_t secondHand = (millis() / 1000) % 60;
    static uint8_t lastSecond = 99;
    
    if( lastSecond != secondHand) {
        lastSecond = secondHand;
        if( secondHand ==  0)  { currentPalette = RainbowColors_p;         currentBlending = LINEARBLEND; }
        if( secondHand == 10)  { currentPalette = RainbowStripeColors_p;   currentBlending = NOBLEND;  }
        if( secondHand == 15)  { currentPalette = RainbowStripeColors_p;   currentBlending = LINEARBLEND; }
        if( secondHand == 20)  { SetupPurpleAndGreenPalette();             currentBlending = LINEARBLEND; }
        if( secondHand == 25)  { SetupTotallyRandomPalette();              currentBlending = LINEARBLEND; }
        if( secondHand == 30)  { SetupBlackAndWhiteStripedPalette();       currentBlending = NOBLEND; }
        if( secondHand == 35)  { SetupBlackAndWhiteStripedPalette();       currentBlending = LINEARBLEND; }
        if( secondHand == 40)  { currentPalette = CloudColors_p;           currentBlending = LINEARBLEND; }
        if( secondHand == 45)  { currentPalette = PartyColors_p;           currentBlending = LINEARBLEND; }
        if( secondHand == 50)  { currentPalette = myRedWhiteBluePalette_p; currentBlending = NOBLEND;  }
        if( secondHand == 55)  { currentPalette = myRedWhiteBluePalette_p; currentBlending = LINEARBLEND; }
    }
}

// This function fills the palette with totally random colors.
void SetupTotallyRandomPalette()
{
    for( int i = 0; i < 16; i++) {
        currentPalette[i] = CHSV( random8(), 255, random8());
    }
}

// This function sets up a palette of black and white stripes,
// using code.  Since the palette is effectively an array of
// sixteen CRGB colors, the various fill_* functions can be used
// to set them up.
void SetupBlackAndWhiteStripedPalette()
{
    // 'black out' all 16 palette entries...
    fill_solid( currentPalette, 16, CRGB::Black);
    // and set every fourth one to white.
    currentPalette[0] = CRGB::White;
    currentPalette[4] = CRGB::White;
    currentPalette[8] = CRGB::White;
    currentPalette[12] = CRGB::White;
    
}

// This function sets up a palette of purple and green stripes.
void SetupPurpleAndGreenPalette()
{
    CRGB purple = CHSV( HUE_PURPLE, 255, 255);
    CRGB green  = CHSV( HUE_GREEN, 255, 255);
    CRGB black  = CRGB::Black;
    
    currentPalette = CRGBPalette16(
                                   green,  green,  black,  black,
                                   purple, purple, black,  black,
                                   green,  green,  black,  black,
                                   purple, purple, black,  black );
}


// This example shows how to set up a static color palette
// which is stored in PROGMEM (flash), which is almost always more
// plentiful than RAM.  A static PROGMEM palette like this
// takes up 64 bytes of flash.
const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM =
{
    CRGB::Red,
    CRGB::Gray, // 'white' is too bright compared to red and blue
    CRGB::Blue,
    CRGB::Black,
    
    CRGB::Red,
    CRGB::Gray,
    CRGB::Blue,
    CRGB::Black,
    
    CRGB::Red,
    CRGB::Red,
    CRGB::Gray,
    CRGB::Gray,
    CRGB::Blue,
    CRGB::Blue,
    CRGB::Black,
    CRGB::Black
};



