#!/usr/bin/env python2

from __future__ import print_function
from __future__ import division

import grid
import rotationMotorTest
import RPi.GPIO as GPIO
import serial
import time
import os

import math

number_of_nodes = 49
course_nodes = grid.Grid(number_of_nodes)

#motor control
from BrickPi import *  # import BrickPi.py file to use BrickPi operations
from MultiMotorDriving import *  # So can do precision motor rotations


#initialize motor
left_motor = PORT_B
right_motor = PORT_A
motor = rotationMotorTest.MotorControls(left_motor, right_motor)

#initialize serial communication
#ser = serial.Serial('/dev/ttyUSB1',9600, timeout = 2)   #use with redboard

ser = serial.Serial('/dev/ttyAMA0',9600, timeout = 2)  #use with arduino uno

###function for shutdown pi when red button is pressed
##def Shutdown(channel):
##  # time.sleep(4)
##   GPIO.cleanup()
##   os.system.__call__(KeyboardInterrupt)
##   # was shutdown,  changed to keyboard interrupt.  to just exit program.
##   # shuts down entire operating system
##   # os.system("python /home/pi/end.py")

#function for shutdown pi when red button is pressed

def system_action(STOPBUTTON):
   print("Stop Button press detected.")
   button_press_timer=0
   while True:
      if (GPIO.input(STOPBUTTON) == False) : # while button is still pressed down
          button_press_timer += 1 # keep counting until button is released
      else: # button is released, figure out for how long
          if (button_press_timer > 7) : # pressed for > 7 seconds
              print ("long press > 7 : ", button_press_timer)
              Shutdown()
          elif (button_press_timer > 3) : # press for > 3 < 5 seconds
              print ("short press > 3 < 5 : ", button_press_timer)
              Reboot()
          elif (button_press_timer > 1) : # press for > 1 < 3 seconds
              print ("short press > 1 < 3 : ", button_press_timer)
              HaltRobot()
          button_press_timer = 0
      sleep(1)

def system_action(STARTBUTTON):
   # time.sleep(4)
   StartMain()
   # was shutdown,  changed to keyboard interrupt.  to just exit program.
   #shuts down entire operating system


def HaltRobot(channel):
  # time.sleep(4)
  print ("HaltRobot button test confirmed")
  #motor.move_bot(action_to_take)  # Send command to move the bot
  # os.system.KeyboardInterrupt  #shuts down entire operating system
  # code to send stop to motors here
  # code to restart main program here,
  # return to wait for green button, or resume

def Shutdown(channel):
  # time.sleep(4)
  print ("Shutdown button test confirmed")
  # code to send stop to motors here
  # GPIO.cleanup()
  # os.system("sudo shutdown -h now")  #shuts down entire operating system

def Reboot(channel):
  # time.sleep(4)
  print ("Reboot button test confirmed")
  # code to send stop to motors here
  # GPIO.cleanup()
  # os.system("sudo reboot")  #shuts down entire operating system

def StartMain(channel):
  # time.sleep(4)
  print ("Start button pressed")
  main()
  # code to send stop to motors here
  # GPIO.cleanup()
  # os.system("sudo reboot")  #shuts down entire operating system


#setup interrupts for start and stop push buttons
STOPBUTTON = 04
STARTBUTTON = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(04, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(STOPBUTTON, GPIO.FALLING, bouncetime = 400)
GPIO.add_event_detect(STARTBUTTON, GPIO.FALLING, bouncetime = 400)

#setup interrupts for stop push button
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(04, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(04, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)#switch 07 back to 11


#code for direction to go
#0 go straight
#1 turn left, go straight
#2 turn left, go straight, turn left
#3 turn right, go straight, turn right
#4 stop
#5 straight, right
#6 straight, left
#7 right
#8 left


#call motor object for controlling the motor
#perimeter search. will continue to run as long as the last node hasn't been reached
def PerimeterSearch(course_nodes):
    course_nodes.is_searching = 1
   # course_nodes[course_nodes.current_node].traversed = True
    # get emf and ir values
    #sendAndReceiveValue('c', int(course_nodes.current_node), 'y')
   # motor.fwd()
    #perimeter search. will continue to run as long as the last node hasn't been reached
    while course_nodes.is_searching == 1:
        course_nodes[course_nodes.current_node].traversed = 1

        #get EMF value from Arduino
      #  EMF = ser.read()
        #print (EMF)
        sendAndReceiveValue('c', int(course_nodes.current_node), 'r')
        action_to_take = course_nodes.next_node_perim()
        #action_to_take = course_nodes.next_node()
        if action_to_take == 0:
            inp = 'w'       #robot isn't at a corner. go straight.
        elif action_to_take == 6:
            inp = '.'       #robot is right before the corner. go straight, turn left (will need to change code to do this)

      #  motor.move_bot(inp)  # Send command to move the bot
        time.sleep(1)  # sleep for 10 ms

    # 0 go straight
    # 1 turn left, go straight
    # 2 turn left, go straight, turn left
    # 3 turn right, go straight, turn right
    # 4 stop
    # 5 straight, right
    # 6 straight, left
    # 7 right
    # 8 left
    # 9 180 degree turn
    # 10 turn right, go straight

    
def GridSearch(course_nodes):
    course_nodes.is_searching = 1
    while course_nodes.is_searching == 1:
        course_nodes[course_nodes.current_node].traversed = True
        print ("Grid Search", course_nodes.current_node)
      #  objInFront = '0'
      #  ser.write('a')              #get node values from the Arduino
      #  objInFront = ser.read()     #check if there are any obstacles in front of the robot
      #  if objInFront == '0':       #if there are any obstacles in front of the robot, avoid the obstacle
      #     obstacleAvoidance(course_nodes,motor)
        sendAndReceiveValue('c', int(course_nodes.current_node), 'b')
        action_to_take = course_nodes.next_node_grid()
        if action_to_take == 0:
                inp = 'w'       #robot isn't at a corner. go straight.
                print("straight")
        elif action_to_take == 1:
                inp = 'l'       #robot is at beginning of perimeter search. needs to turn into grid
        elif action_to_take == 2:
                inp = 'n'       #robot is at easternmost inner grid
        elif action_to_take == 3:
                inp = 'b'       #robot is at final node. stop
        elif action_to_take == 4:
                inp = 's'       #stop
        elif action_to_take == 10:
                inp = 'p'       #turn 180 degrees
        elif action_to_take == 6:
                inp = '.'       #go straight, turn left
                print ("straight left")
        elif action_to_take == 5:
                inp = 'v'       #go straight, turn right
                print ("straight right")

        #motor.move_bot(inp)  # Send command to move the bot
        time.sleep(.5)  # sleep for 10 ms

def obstacleAvoidance(course_nodes, motor):
   print ("now in obstacle avoidance!")
   startNode = course_nodes.current_node
   startRow = course_nodes[course_nodes.current_node].row_number
   startOrientation = course_nodes.orientation
   course_nodes.avoidingObstacle = True

   if course_nodes[course_nodes.current_node].row_number % 2 == 0:
      motor.move_bot('a')  # turn left
      course_nodes.change_orientation('l')
      motor.move_bot('w')  # go straight
      course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
      motor.move_bot('w')  # go straight
      course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
      motor.move_bot('d')  # turn right
      course_nodes.change_orientation('r')
      motor.move_bot('w')  # go straight
      course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
      motor.move_bot('w')  # go straight
      course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node() 
      motor.move_bot('d')  # turn right
      course_nodes.change_orientation('r')
      motor.move_bot('w')  # go straight
      course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
      motor.move_bot('w')  # go straight
      course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
      motor.move_bot('a')  # turn left
      course_nodes.change_orientation('l')

     # while course_nodes.avoidingObstacle == True:
      #   direction = course_nodes.obstacleAvoidance('e', startRow, evaluateNode(), startNode)
          # motor.move_bot(direction)
          # motor.move_bot('w')  # go straight
       #  time.sleep(3)
       # motor.move_bot('a') #turn robot left to reorient robot

      #course_nodes.change_orientation('l') #reorient direction in node
      #print ("end of obstacle avoidance**********")


   elif course_nodes[course_nodes.current_node].row_number % 2 == 1:
      motor.right()  # turn right
      course_nodes.change_orientation('r')
      motor.fwd() # go straight
      course_nodes.current_node  = course_nodes.current_node + course_nodes.increment_node()
      motor.fwd() # go straight
      course_nodes.current_node  = course_nodes.current_node + course_nodes.increment_node()
      motor.left()  # turn left
      course_nodes.change_orientation('l')
      motor.fwd()  # go straight
      course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
      motor.fwd()  # go straight
      course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
      motor.left()  # turn left
      course_nodes.change_orientation('l')
      motor.fwd()  # go straight
      course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
      motor.fwd()  # go straight
      course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
      motor.right()  # turn right
      course_nodes.change_orientation('r')
      #print ("turning right!")
        #motor.move_bot('d')  # turn right
      #course_nodes.change_orientation('r')

      #while course_nodes.avoidingObstacle:
       #  direction = course_nodes.obstacleAvoidance('o', startRow, evaluateNode(), startNode)
        # motor.move_bot(direction)
           # motor.move_bot('w')
         #time.sleep(3)
        #motor.move_bot('d')#turn robot right to reorient robot
      #course_nodes.change_orientation('r') #reorient direction in node
      #print ("end of obstacle avoidance************")
#def sendValue(number):
def number2Char(number):
   if number == 1:
      return '1'
   elif number == 2:
      return '2'
   elif number == 3:
      return '3'
   elif number == 4:
      return '4'
   elif number == 5:
      return '5'
   elif number == 6:
      return '6'
   elif number == 7:
      return '7'
   elif number == 8:
      return '8'
   elif number == 9:
      return '9'
   else:
      return '0'
   

#def evaluateNode()9
   # ser.write('b')  # get IR sensor values from the Arduino
   # sensor1 = ser.read() #right
   # sensor2 = ser.read() #front
   # sensor3 = ser.read() #left
   # values = {1: sensor1, 2: sensor2, 3: sensor3}
    #return values


#a: see if object is in front of the robot
#b: see if object isto the right of, in front of, or left of the robot
#c: send LED value
#d: send value for seven segment display

def sendAndReceiveValue(actionCode, actionToTake, color):
    
    send = actionCode
    values = ' '

    #
    if actionCode == 'a':
           send += '\n'
           ser.write(send)
           values = ser.read()
    elif actionCode == 'b':
           send += '\n'
           ser.write(send)
           sensor1 = ser.read() #right
           sensor2 = ser.read() #front
           sensor3 = ser.read() #left
           values = {1: sensor1, 2: sensor2, 3: sensor3}
    elif actionCode == 'c':
           if actionToTake < 10:
              print (actionToTake)
              send += '0'
              send += number2Char(actionToTake)
              send += color
              send += '\n'
              print(send)
              ser.write(send)
           else:
              print (actionToTake)
              send += number2Char(math.floor(actionToTake / 10))
              send += number2Char(actionToTake % 10)
              send += color
              send += '\n'
              ser.write(send)
    elif actionCode == 'd':
           send += number2Char(actionToTake)
           send += '\n'
           ser.write(send)
           values = ser.read()
    elif actionCode == 'g':
           send += actionToTake #actionToTake determines which direction we will turn
                                                                             #send header to initialize header value for comparison.
          # send += number2Char(math.floor(actionToTake / 100))             # Should be sent at beginning of turn. 
          # send += number2Char(math.floor((actionToTake % 100) / 10))
         #  send += number2Char(actionToTake % 10)
           send += '\n'
           ser.write(send)
    elif actionCode == 'h':                                                 #send header. Arduino will calculate difference between original 
         #  send += number2Char(math.floor(actionToTake / 100))             #and current heading and return whether or not we are within the threshold
          # send += number2Char(math.floor((actionToTake % 100) / 10))
           #send += number2Char(actionToTake % 10)
           send += '\n'
           ser.write(send)
           heading1 = ser.read()
           heading2 = ser.read()
           heading3 = ser.read()
           heading = value1*100 + values*10 + value3
    else:
           send = actionCode
           send += actionCode

    #print (send)
    return heading

def get_initial_heading(heading):
   if heading > 180:
      # heading orientation
      # positive/ negative planes
      initial_heading = heading - 360;
   else:
      initial_heading = heading;
   return initial_heading

def get_updated_heading(heading):
   if heading > 180:
      # heading orientation
      # positive/ negative planes
      updated_heading = heading - 360;
   else:
      updated_heading = heading;
   return updated_heading

def get_delta_heading(initial_heading,updated_heading):
   delta_heading = updated_heading - initial_heading;
   return delta_heading

# get initial heading before move
def go_forward(initial_heading,updated_heading,delta_heading):
   upper_limit = 5;
   lower_limit = -5;
   # correct rightward heading
   if delta_heading > upper_limit:
      while delta_heading > upper_limit:
         # turn left
         motor.movement(-1,1,100,100)
         delta_heading = get_delta_heading(initial_heading,updated_heading);
         # initial heading before enters function, reference initial heading
   # correct leftward heading
   if delta_heading < lower_limit:
      while heading_delta < lower_limit:
         # turn right 
         motor.movement(1,-1,100,100)
         delta_heading = get_delta_heading(initial_heading,updated_heading);
         # initial heading before enters function, reference initial heading
   return

# get initial heading before move
def go_right(initial_heading,updated_heading_delta_heading):
   # correct heading while turning right
   upper_limit = 95;
   lower_limit = 85;
   # correct overturn
   if delta_heading > upper_limit:
      while delta_heading > upper_limit:
         motor.movement(-1,1,100,100)
         delta_heading = get_delta_heading(initial_heading,updated_heading);
   #correct underturn
   if delta_heading < lower_limit:
      while delta_heading < lower_limit:
         motor.movement(1,-1,100,100)
         delta_heading = get_delta_heading(initial_heading,updated_heading);
   return

# get initial heading before move
def go_left(initial_heading,updated_heading_delta_heading):
   # correct heading while turning right
   upper_limit = -95;
   lower_limit = -85;
   # correct overturn
   if delta_heading > upper_limit:
      while delta_heading > upper_limit:
         motor.movement(1,-1,100,100)
         delta_heading = get_delta_heading(initial_heading,updated_heading);
   #correct underturn
   if delta_heading < lower_limit:
      while delta_heading < lower_limit:
         motor.movement(-1,1,100,100)
         delta_heading = get_delta_heading(initial_heading,updated_heading);
   return


   
#def UpdateValues():



def main():
   
   #bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
   time.sleep(4) #need this always before code begins! 4 seems to work okay


   #sendAndReceiveValue('c', 1, 'p')
 #  print (sendAndReceiveValue('h', 320, 0))
     # time.sleep(2)
 #  print (sendAndReceiveValue('a', 14, 'b'))
  # print (sendAndReceiveValue('b', 14, 'b'))
  # print (sendAndReceiveValue('d', 4, 'r'))
   #print (sendAndReceiveValue('c', 1, 'b'))
   #time.sleep(1)
  # print (sendAndReceiveValue('c', 2, 'r'))
  # time.sleep(1)
 #  print (sendAndReceiveValue('c', 3, 'g'))
  # time.sleep(1)
  # print (sendAndReceiveValue('c', 4, 'p'))
  # time.sleep(1)
   #stillTurning = sendAndReceiveValue('g', 'z', 'z')
   #stillTurning = sendAndReceiveValue('h', 'z', 'z')


   #testing
   #while stillTurning != 'g':
   #   motor.movement(1,-1,100,100) #left turn
     # getHeading = sendAndReceiveValue('h', 'z', 'z')
     #call header comparison code
   #   print (stillTurning)

#********************************
#*   Main Search Routine        *
#********************************

   course_nodes.initialize()
   print ("Course grid initialized.")
   PerimeterSearch(course_nodes)
   print ("Perimeter Search Complete.")
 
   GridSearch(course_nodes)
   print ("Grid Search Complete.")
 
#
#
   time.sleep(.01)
   print ("done")
   while True:
      time.sleep(.01)

if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      GPIO.cleanup()   # clean up GPIO on CTRL+C exit.

GPIO.cleanup()
