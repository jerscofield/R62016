/* Interrupt on a button
 * By: Jeffrey Hundstad <we0a@arrl.net> 2015-03-09
 * Documentation on AttachInterrupt:
 *  http://arduino.cc/en/Reference/AttachInterrupt 


/* PIN definitions */
const byte led_pin = LED_BUILTIN;  // built in LED
const byte but_pin = 2;            // Button on pin-2, internal pullup
const int buttonPin = 3;     // the number of the pushbutton pin
int buttonState = 0;

/* Volatile variables modified in the ISR */
volatile boolean led_state = LOW;
volatile unsigned int last_but_ptime = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
  pinMode(led_pin, OUTPUT);
  pinMode(but_pin, INPUT_PULLUP);
  /*
   * attachInterrupt(interrupt, ISR, mode)
   *  interrupt = [0 == pin 2, 1 == pin 3]
   *  MODE = [LOW, CHANGE, RISING, FALLING]
   */
  attachInterrupt(0, blink, RISING);
}

/* Show the led_state on the internal LED, it is changed in the ISR */
void loop()
{
    buttonState = digitalRead(buttonPin);
  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH:
    if (buttonState == HIGH) {
    Serial.write('1');
  } else {  
    Serial.write('2');
  }
    digitalWrite(led_pin, led_state);
}


/* Intended to be attached as an ISR */
/* Change the led_state but on as fast as PRESS_DELAY */
const unsigned int PRESS_DELAY = 100; /* milliseconds */
void blink()
{
  unsigned int but_ptime = millis();
  if ( (but_ptime - last_but_ptime) > PRESS_DELAY) {
    last_but_ptime = but_ptime;
    led_state = !led_state;
  }
}


