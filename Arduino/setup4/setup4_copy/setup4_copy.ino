#include <EEPROM.h>

#include <FastLED.h>
#include <Arduino.h>
#include <SharpIR.h>
//#include <string>

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

Adafruit_BNO055 bno = Adafruit_BNO055(55);


//initialize LED Matrix Display
#define LED_PIN     7
#define NUM_LEDS    55
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
#define kMatrixWidth 8
#define kMatrixHeight 8
#define UPDATES_PER_SECOND 100
CRGB leds[kMatrixWidth * kMatrixHeight];
const uint8_t ledSpot[] = {14, 6, 5, 4, 3, 2, 1, 0, 14, 13, 12, 11, 10, 9, 8, 22, 21, 20, 19, 18, 17, 16, 30, 29, 28, 27, 26, 25, 24, 38, 37, 36, 35, 34, 33, 32, 46, 45, 44, 43, 42, 41, 40, 54, 53, 52, 51, 50, 49, 48, 55};


//initialize IR values and functions
#define model 20150
#define ir A0    //front sensor
#define ir2 A1
#define ir3 A2
SharpIR sharp1(ir, 25, 93, model);
SharpIR sharp2(ir2, 25, 93, model);
SharpIR sharp3(ir3, 25, 93, model);
char ObjInFront(SharpIR);  //get whether or not obstacle is in front of robot

//7 segment display
const int latchPin = 2; // pin 12
const int dataPin = 3; // pin 14
const int clockPin = 4; // pin 11



//function declarations
//converts a string array of values to an integer  
void ledValues(int, char);
int convertStr2Int(char digit);
void restartLEDs(void);
void write7Seg(char);
char IMUTurn(int);


//void ledValues(char *typeOfNode);
//int** convert1Dto2d(int *1dArray);

//initializers for serial communication
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
int previousHeader;


void setup() {
    Serial.begin(9600);
    delay( 3000 ); // power-up safety delay

    //initialize LED object
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
    FastLED.setBrightness(  96 );
  //pinmodes for 7 segment LED  
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
    Serial.print("Here1");
  inputString.reserve(200);
    Serial.print("Here2");
  previousHeader = 0;int sensorValue = 0;  // variable to store the value coming from the sensor
    Serial.print("Here3");
    leds[ledSpot[1]] = CRGB::Yellow;  // turn yellow on home square at init.
      Serial.print("Here4");
  FastLED.show();
    Serial.print("Here5");
  bno.setExtCrystalUse(true);
    Serial.print("Here6");
}

void loop()
{
  Serial.print("Here7");
  int updated_heading;
  int heading_delta;
  char fwd;
  char turn;
  
  
    // print the string when a newline arrives:
  if (stringComplete) {
    char front;
    char right;
    char left;
    String value2Send = "";
    
    char actionType = inputString[0];
   // Serial.print(actionType);
    int number = 10*convertStr2Int(inputString[1]) + convertStr2Int(inputString[2]);
    int headerNumber = 100*convertStr2Int(inputString[1]) + 10*convertStr2Int(inputString[2]) + convertStr2Int(inputString[3]);
    char sevSegNumber = inputString[1];
    char gridType = inputString[3];
    
 switch(actionType){
    case 'a':  front = objInFront(sharp1);//get front IR sensor from PI
               value2Send += front;
               value2Send += '\n';
               Serial.write(front);         
               break;
    case 'b':  right = objInFront(sharp1); //get front, right, and left values from IR sensor
               front = objInFront(sharp2);
               left = objInFront(sharp3);
               value2Send += right;
               value2Send += front;
               value2Send += left;
               value2Send += '\n';
               //irValue2Send.append(front);
               //irValue2send.append()
               //Serial.print(right);
               //Serial.print(front);
               Serial.println(value2Send);
               break;
    case 'c':  ledValues(number, gridType);   //updates the matrix
              Serial.flush();
              break;
    case 'e':                         //used for testing the matrix. remove later
              //Serial.print(typeOfNode[1]);
              //Serial.print(typeOfNode[2]);
              Serial.flush();
              break;
    case 'd': write7Seg(sevSegNumber);
              //Serial.print(ledNumber);
              Serial.flush();              
              break;
    case 'f': //restartLEDs();
              Serial.flush();
              break;
    case 'g' : 
     //   updated_heading = get_updated_heading();
      //  heading_delta = get_heading_delta(updated_heading);
       // fwd = move_fwd(heading_delta);
        Serial.write(fwd);
        Serial.flush();
        break;
      
    case 'h': 
        Serial.print("Test Here!");
     //   updated_heading = get_updated_heading();
      //  heading_delta = get_heading_delta(updated_heading);
       // turn = move_turn(heading_delta);
        Serial.write(turn);
        Serial.flush();
        break;
      
    
    default:
              Serial.write('z');
              Serial.flush();
       //put numbers on grids case 'c': put numbers on grids
  }                        
    inputString = "";
    stringComplete = false;
  }

}




//change color of the LED on the matrix display
//takes strng from the serial communication
//converts string to a number for which LED should display
//and a character for which color the LED should change to
//and changes the colors in the matrix accordingly
void ledValues(int number, char typeOfString)
{
       

  switch (typeOfString){
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
  //  typeOfNode[number] = gridSpot;
    FastLED.show();
    return;
                                                   
//}
}



//used with the ledValues function
//takes a number in the form of a character
//converts the character number to an integer number
//returns the integer number
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

//write values to the 7 segment display
void write7Seg(char number){
  

// JScofield 3-19-17.  added extra clock high and low to push data through the storage register.  Converted values to hex.   

  switch (number){
    case('2'):
              digitalWrite(latchPin, HIGH);
              shiftOut(dataPin, clockPin, MSBFIRST, 0x5B);//shiftOut(dataPin, clockPin, MSBFIRST, 091);
              digitalWrite(latchPin, LOW);
              digitalWrite(latchPin, HIGH);
              digitalWrite(latchPin, LOW);
              break;
    case('3'):  
              digitalWrite(latchPin, HIGH);
              shiftOut(dataPin, clockPin, MSBFIRST, 0x4F);//shiftOut(dataPin, clockPin, MSBFIRST, 079);
              digitalWrite(latchPin, LOW);
              digitalWrite(latchPin, HIGH);
              digitalWrite(latchPin, LOW);
              break;
    case('4'):
              digitalWrite(latchPin, HIGH);
              shiftOut(dataPin, clockPin, MSBFIRST, 0x66);//shiftOut(dataPin, clockPin, MSBFIRST, 0102);
              digitalWrite(latchPin, LOW);
              digitalWrite(latchPin, HIGH);
              digitalWrite(latchPin, LOW);
              break;
    case('5'):
              digitalWrite(latchPin, HIGH);
              shiftOut(dataPin, clockPin, MSBFIRST, 0x6D);//shiftOut(dataPin, clockPin, MSBFIRST, 0109);
              digitalWrite(latchPin, LOW);
              digitalWrite(latchPin, HIGH);
              digitalWrite(latchPin, LOW);
              break;
    case('6'):
              digitalWrite(latchPin, HIGH);
              shiftOut(dataPin, clockPin, MSBFIRST, 0x7C);//shiftOut(dataPin, clockPin, MSBFIRST, 0124);
              digitalWrite(latchPin, LOW);
              digitalWrite(latchPin, HIGH);
              digitalWrite(latchPin, LOW);
              break;
    case('1'):
              digitalWrite(latchPin, HIGH);
              shiftOut(dataPin, clockPin, MSBFIRST, 0x06);//shiftOut(dataPin, clockPin, MSBFIRST, 6);
              digitalWrite(latchPin, LOW);
              digitalWrite(latchPin, HIGH);
              digitalWrite(latchPin, LOW);
              break;
    default:
              digitalWrite(latchPin, HIGH);
              shiftOut(dataPin, clockPin, MSBFIRST, 0x00);//shiftOut(dataPin, clockPin, MSBFIRST, 000);
              digitalWrite(latchPin, LOW);
              digitalWrite(latchPin, HIGH);
              digitalWrite(latchPin, LOW);
              break;

  } 
    return;
}


//checks for obstacle in front of the robot
//I think that this sensor only detects within 10 t0 80 CM
//should be able to check 3 blocks
char objInFront(SharpIR sharp){
  int dis = sharp.distance();
  
  if(dis > 40)
    return '1';  //there is no obstacle in front of sensor
   else 
     return '0';  //there is an obstacle in front of sensor
}




void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

/*
// get the updated heading reading
int get_updated_heading() {
  int updated_heading;
  sensors_event_t event;
  bno.getEvent(&event);
  updated_heading = event.orientation.x;
  return updated_heading;
}

// calculate the heading delta
int get_heading_delta(int updated_heading) {
  int heading_delta;
  if (updated_heading > 180) {
    updated_heading = updated_heading - 360;
    heading_delta = updated_heading;
  }
  else {
    heading_delta = updated_heading;
  }
  return heading_delta;
}

// move forward with l/r compensation
char move_fwd(int heading_delta) {
  char left = 'l';
  char right = 'r';
  char forward = 'n';
  if (heading_delta > 5 && heading_delta < 180) {
    // send command to turn left to correct
    return left;
  }
  if (heading_delta < -5 && heading_delta > -180) {
    // send command to turn right to correct
    return right;
  }
  else {
    // send command to continue forward
    return forward;
  }
}

// turn l/r, indicate when done
char move_turn(int heading_delta) {
  char continue_turn = 'g';
  char end_turn = 'e';
  if (abs(heading_delta) < 90) {
    return continue_turn;
  }
  return end_turn;
}
*/


