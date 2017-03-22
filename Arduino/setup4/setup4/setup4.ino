#include <FastLED.h>
#include <Arduino.h>
#include <SharpIR.h>
//#include <string>




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
int convertChar2Int(char);
char convertInt2Char(int);
void restartLEDs(void);
void write7Seg(char);
String IMUTurn(void);


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
  inputString.reserve(200);
  previousHeader = 0;int sensorValue = 0;  // variable to store the value coming from the sensor
    leds[ledSpot[1]] = CRGB::Yellow;  // turn yellow on home square at init.
  FastLED.show();
}

void loop()
{
  
  
    // print the string when a newline arrives:
  if (stringComplete) {
    char front;
    char right;
    char left;
    String value2Send = "";
    
    char actionType = inputString[0];
   // Serial.print(actionType);
    int number = 10*convertChar2Int(inputString[1]) + convertChar2Int(inputString[2]);
    int headerNumber = 100*convertChar2Int(inputString[1]) + 10*convertChar2Int(inputString[2]) + convertChar2Int(inputString[3]);
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

              break;
    case 'e':                         //used for testing the matrix. remove later
              //Serial.print(typeOfNode[1]);
              //Serial.print(typeOfNode[2]);
              Serial.flush();
              break;
    case 'd': write7Seg(sevSegNumber);            
              break;
    case 'f': //restartLEDs();
              Serial.flush();
              break;
    case 'g': previousHeader = headerNumber;    //change so that all of the header values come from the library
              break;
    case 'h': value2Send = IMUTurn();        //code for comparing headers
              value2Send += '\n';
              Serial.println(value2Send);
              //Serial.flush();
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
int convertChar2Int(char digit){
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


//used with the ledValues function
//takes a number in the form of a character
//converts the character number to an integer number
//returns the integer number
char convertInt2Char(int digit){
  char digitAsChar = 0;
  
  switch(digit){
    case 0:
      digitAsChar = '0';
      break;
    case 1:
      digitAsChar = '1';
      break;
    case 2:
      digitAsChar = '2';
      break;
    case 3:
      digitAsChar = '3';
      break;
    case 4:
      digitAsChar = '4';
      break;
    case 5:
      digitAsChar = '5';
      break;
    case 6:
      digitAsChar = '6';
      break;
    case 7:
      digitAsChar = '7';
      break;
    case 8:
      digitAsChar = '8';
      break;
    case 9:
      digitAsChar = '9';
      break;  
    default:
      digitAsChar = '0';    
        
  }
  return digitAsChar;

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
  int dis = abs(sharp.distance());
  
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


String IMUTurn(void){
  String returnHeader = "";
  
  int header;
  //put code for get header here
  
   returnHeader += convertInt2Char(header / 100);
   returnHeader += convertInt2Char((header  % 100) / 10);
   returnHeader += convertInt2Char(header  % 10);
   
  
  
  /*if (newHeader > previousHeader){
    previousHeader = newHeader;
    return '0';
  }
  else{
    previousHeader = newHeader;
    return '1';
  }
  */
  return returnHeader;
}


