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


#initialize motor
# left_motor = PORT_B
# right_motor = PORT_A
# motor = rotationMotorTest.MotorControls(left_motor, right_motor)




#function for shutdown pi when red button is pressed
#def Shutdown(channel):
#	GPIO.cleanup()
#	os.system("sudo shutdown -h now")


#0 go straight
#1 go straight, turn left
#2 stop
#call motor object for controling the motor
#perimeter search. will continue to run as long as the last node hasn't been reached
def PerimeterSearch(course_nodes):
    course_nodes.is_searching = 1
    #perimeter search. will continue to run as long as the last node hasn't been reached
    while course_nodes.is_searching == 1:
        print ("Perimeter Search", course_nodes.current_node)

	    #update sensor values
     #   ser.write('G');

        #get EMF value from Arduino
      #  EMF = ser.read()
        #print (EMF)
        
       # ir_sensor = ser.read()
        #print (ir_sensor)
        
	action_to_take = course_nodes.next_node_perim()
        #action_to_take = course_nodes.next_node()
        
        if action_to_take == 0:
            inp = 'w'       #robot isn't at a corner. go straight.
        elif action_to_take == 1:
            inp = 'i'       #robot is right before the corner. go straight, turn left (will need to change code to do this)
        elif action_to_take == 2:
            inp = 's'       #robot is at a corner. does a half turn onto the next node
            
      #  motor.move_bot(inp)  # Send command to move the bot
        time.sleep(.5)  # sleep for 10 ms

#0 go straight
#1 turn left, go straight
#2 turn left, go straight, turn left
#3 turn right, go straight, turn right
#4 stop
def GridSearch(course_nodes):
    course_nodes.is_searching = 1
    while course_nodes.is_searching == 1:
    	print ("Grid Search", course_nodes.current_node)
	#update sensor values
        #if objInFront:
            #obstacleAvoidance(course_nodes,motor)
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


#0 go straight
#1 turn left, go straight
#2 turn left, go straight, turn left
#3 turn right, go straight, turn right
#4 stop
#5 turn right
#6 turn left
#def obstacleAvoidance(course_nodes, motor):
 #   startRow = course_nodes[course_nodes.current_node].row_number
  #  startOrientation = course_nodes.orientation
   # course_nodes.avoidingObstacle = True


 #   if course_nodes[course_nodes.current_node].row_number % 2 == 0:
#        motor.move_bot('a') #turn left
  #      changeOrientation()

     #   while course_nodes.avoidingObstacle == True:
   #         evaluateNode() #determine if there are any obstacles to the right, in front of, or left of the robot
    #        obstacleAvoidance('e', startRow)

      #  turnDirection(direction)
       # changeOrientation()
       # motor.move_bot('w') #go straight
            #change current node

    #if course_nodes[course_nodes.current_node].row_number % 2 == 1:
     #   motor.move_bot('d') #turn right
      #  changeOrientation()

       # while course_nodes.avoidingObstacle:
            #will need to put a dictionary or something in here to show what values we get when we use the IR sensors
        #    evaluateNode() #determine if there are any obstacles to the right, in front of, or left of the robot
         #   obstacleAvoidance('o', startRow)

          #  turnDirection(direction)
           # changeOrientation()
            #straight()
            #change current node

    #should maybe create a separate function for this inside the grid class.
    #reorient()


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
  #  print (course_nodes.current_node)
  #  for i in range(49):
#	print("Node Number", i, " Node Column", course_nodes[i].col_number, " Node Row", course_nodes[i].row_number)
    #PerimeterSearch(course_nodes, motor)
    #GridSearch(course_nodes, motor)


    PerimeterSearch(course_nodes)
    GridSearch(course_nodes)

    while 1:
        time.sleep(.01)
	print ("done")

if __name__ == "__main__":
    main()

