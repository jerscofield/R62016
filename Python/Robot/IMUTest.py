from __future__ import print_function
from __future__ import division
#from binascii import hexlify

import grid
#import rotationMotorTest
#import RPi.GPIO as GPIO
import serial
import time
import os

#IMU Files
import logging
import sys
import math

#motor control
#from BrickPi import *  # import BrickPi.py file to use BrickPi operations
#from MultiMotorDriving import *  # So can do precision motor rotations

#IMU
from Adafruit_BNO055 import BNO055

#initialize motor and IMU
# left_motor = PORT_B
# right_motor = PORT_A
# motor = rotationMotorTest.MotorControls(left_motor, right_motor)
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=1


# more IMU stuff
# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')



#function for shutdown pi when red button is pressed
#def Shutdown(channel):
#	GPIO.cleanup()
#	os.system("sudo shutdown -h now")


#p: left IMU turn
#l: right IMU turn
#m: go straight
def TurnLeft():
    heading, roll, pitch = bno.read_euler()

    #motor will continue to turn as long as the IMU is does not recognize a whole turn
    while abs(heading) < 90:
        # motor.move_bot('p')  # Send command to move the bot
        heading, roll, pitch = bno.read_euler()

    #recalibrate IMU


# p: use IMU to turn right
# l: right IMU turn
#m: go straight
def TurnRight():
    heading, roll, pitch = bno.read_euler()

    #motor will continue to turn as long as the IMU is does not recognize a whole turn
    while abs(heading) < 90:
        # motor.move_bot('p')  # Send command to move the bot
        heading, roll, pitch = bno.read_euler()

    # recalibrate IMU


# p: use IMU to turn right
# l: right IMU turn
# m: go straight
def Turn180():
    heading, roll, pitch = bno.read_euler()

    # motor will continue to turn as long as the IMU is does not recognize a whole turn
    while abs(heading) < 180:
        # motor.move_bot('p')  # Send command to move the bot
        heading, roll, pitch = bno.read_euler()

    # recalibrate IMU

def TurnDegrees(heading1):

    while heading1 > 0:



        heading1 = heading2


# p: use IMU to turn right
# l: right IMU turn
#m: go straight 3 inches
def GoForward():
    #reset IMU
    # three different movements make the distance of one node
    motor.mov_bot_amount(1)

    for i in range(2):
        heading, roll, pitch = bno.read_euler()
        heading = abs(heading)

        #determine length to drive
        widthOffInit = math.sin(heading)
        lengthOffPost = 2 - math.cos(heading)
        angleToTurn = math.arctan(widthOffInit/lengthOffPost)
        lengthToDrive = widthOffInit / (math.sin(angleToTurn))

        TurnDegrees(heading + angleToTurn)

        motor.mov_bot_amount(lengthToDrive)
        #straighten up -- will need to think about this code a bit


    # recalibrate IMU





#0 go straight
#1 go straight, turn left
#2 stop
#call motor object for controling the motor
#perimeter search. will continue to run as long as the last node hasn't been reached
def PerimeterSearch(course_nodes, motor):
    course_nodes.is_searching = 1
    #perimeter search. will continue to run as long as the last node hasn't been reached
    while course_nodes.is_searching == 1:
        print ("Perimeter Search", course_nodes.current_node)

	    #update sensor values
        ser.write('G');

        #get EMF value from Arduino
        EMF = ser.read()
        #print (EMF)
        
        ir_sensor = ser.read()
        #print (ir_sensor)
        
	action_to_take = course_nodes.next_node_perim()
        #action_to_take = course_nodes.next_node()
        
        if action_to_take == 0:
            inp = 'w'       #robot isn't at a corner. go straight.
        elif action_to_take == 1:
            inp = 'i'       #robot is right before the corner. go straight, turn left (will need to change code to do this)
        elif action_to_take == 2:
            inp = 's'       #robot is at a corner. does a half turn onto the next node
            
        motor.move_bot(inp)  # Send command to move the bot
        time.sleep(.5)  # sleep for 10 ms

#0 go straight
#1 turn left, go straight
#2 turn left, go straight, turn left
#3 turn right, go straight, turn right
#4 stop
def GridSearch(course_nodes, motor):
    course_nodes.is_searching = 1
    while course_nodes.is_searching == 1:
   	print ("Grid Search", course_nodes.current_node, " self.orientation: ", course_nodes.orientation)
	#update sensor values
        action_to_take = course_nodes.next_node_grid()
        if action_to_take == 0:
            inp = 'w'       #robot isn't at a corner. go straight.
        elif action_to_take == 1:
            inp = 'i'       #robot is at beginning of perimeter search. needs to turn into grid
        elif action_to_take == 2:
            inp = 'j'       #robot is at easternmost inner grid
        elif action_to_take == 3:
            inp = 's'       #robot is at westernmost inner grid
        elif action_to_take == 4:
            inp = 't'       #stop
       # motor.move_bot(inp)  # Send command to move the bot
        time.sleep(.5)  # sleep for 10 ms

#def UpdateValues():

#setup interrupts for stop push button
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(11, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)


def main():
    number_of_nodes = 100
    course_nodes = grid.Grid(number_of_nodes)
    #left_motor = PORT_B
    #right_motor = PORT_A
    #motor = rotationMotorTest.MotorControls(left_motor, right_motor)
    #bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
   
   # ser = serial.Serial('/dev/ttyACM1',9600)
  #  has_been_pressed = 0
  #  while has_been_pressed == 0:
  #      read_serial=ser.read()
  #      if (read_serial == '1'):
   #         has_been_pressed = 1
 #   course_nodes[course_nodes.current_node].cache_present
   # time.sleep(20)
      
   #  BrickPiSetup()  # Setup the serial port for communication (***NB*** APP MUST BE RUN IN SUDO MODE ***NB***)
   #  self.leftMotor = PORT_B
   #  self.rightMotor = PORT_A
   #  self.motors = [leftMotor, rightMotor]
   # BrickPi.MotorEnable[leftMotor] = 1  # Don't turn these off - set its speed to 0 to stop a motor
   # BrickPi.MotorEnable[rightMotor] = 1
   # BrickPiSetupSensors()  # Send the properties of sensors to BrickPi
   # BrickPi.Timeout = 30000  # So motors won't stop cause of lack of contact (30 seconds)
   # BrickPiSetTimeout()  # (BrickPi's default is 250 msec (really meeses with motor reliability))
	
    course_nodes.initialize()
    print (course_nodes.current_node)
    for i in range(49):
	print("Node Number", i, " Node Column", course_nodes[i].col_number, " Node Row", course_nodes[i].row_number)
    #PerimeterSearch(course_nodes, motor)
    #GridSearch(course_nodes, motor)

    while 1:
        time.sleep(.01)
	print ("done")

if __name__ == "__main__":
    main()

