#!/usr/bin/env python2

from __future__ import print_function
from __future__ import division

import grid
import rotationMotorTest
import RPi.GPIO as GPIO
import serial
import time
from time import sleep
import subprocess
import os
import math

#motor control
from BrickPi import *  # import BrickPi.py file to use BrickPi operations
from MultiMotorDriving import *  # So can do precision motor rotations

#initialize motor
left_motor = PORT_B
right_motor = PORT_A
motor = rotationMotorTest.MotorControls(left_motor, right_motor)

#initialize arm lift servo motor
#Lift_motor = PORT_C
#Liftmotor = rotationMotorTest.MotorControls(Lift_motor)

#initialize serial communication
#ser = serial.Serial('/dev/ttyUSB0',9600, timeout = 2)   #use with redboard
ser = serial.Serial('/dev/ttyACM0',9600, timeout = 2)  #use with arduino uno


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
              self.Shutdown()
          elif (button_press_timer > 3) : # press for > 3 < 5 seconds
              print ("short press > 3 < 5 : ", button_press_timer)
              self.Reboot()
          elif (button_press_timer > 1) : # press for > 1 < 3 seconds
              print ("short press > 1 < 3 : ", button_press_timer)
              self.HaltRobot()
          button_press_timer = 0
      sleep(1)

#setup interrupts for stop push button
STOPBUTTON = 04
GPIO.setmode(GPIO.BCM)
GPIO.setup(04, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(STOPBUTTON, GPIO.FALLING, bouncetime = 400)
#GPIO.add_event_detect(04, GPIO.FALLING, callback = STOPBUTTON, bouncetime = 2000)


#GPIO.add_event_detect(STOPBUTTON, GPIO.FALLING, callback=system_action, bouncetime=200)
# setup the thread, detect a falling edge on channel 04 and debounce it with 200mSec

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
    while course_nodes.is_searching == 1:
       # course_nodes[course_nodes.current_node].traversed = True  #don't keep this code, probably

      #*******************put "get node data" code in here**************
        #course_nodes[current_node].node_type = 
      #depending on what type of values we received from the capacitive sensor, change color code

        #update matrix display via Arduino
        sendAndReceiveValue('c', int(course_nodes.current_node), course_nodes[course_nodes.current_node].node_type)
        action_to_take = course_nodes.next_node_perim()


        motor.move_bot(action_to_take)  # Send command to move the bot
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


      #*******************put "get node data" code in here**************
        #course_nodes[current_node].node_type = 
        #depending on what type of values we received from the capacitive sensor, change color code

         #update matrix display via Arduino
       # sendAndReceiveValue('c', int(course_nodes.current_node), course_nodes[course_nodes.current_node].node_type)
       
        course_nodes[course_nodes.current_node].traversed = True

        #update matrix display via Arduino
       # sendAndReceiveValue('c', int(course_nodes.current_node), course_nodes[course_nodes.current_node].node_type)
        action_to_take = course_nodes.next_node_grid()

         #determine if there in an obstacle in front of the robot
     #   objInFront = sendAndReceiveValue('a', 'z', 'z')
      #  if objInFront == '0':       #if there are any obstacles in front of the robot, avoid the obstacle
       #    obstacleAvoidance(course_nodes, motor)
           
    #    sendAndReceiveValue('c', int(course_nodes.current_node), 'b')
     #   action_to_take = course_nodes.next_node_grid()

        motor.move_bot(action_to_take)  # Send command to move the bot
        time.sleep(.5)  # sleep for 10 ms

def obstacleAvoidance(course_nodes, motor):
   print ("now in obstacle avoidance!")
   startNode = course_nodes.current_node
   startRow = course_nodes[course_nodes.current_node].row_number
   startOrientation = course_nodes.orientation
   course_nodes.avoidingObstacle = True

   #if we are in an even row, do this obstacle avoidance
   #if course_nodes[course_nodes.current_node].row_number % 2 == 0:
   course_nodes.change_orientation('l')
   motor.move_bot(1)  # turn left, go straight
   course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
   course_nodes.change_orientation('r')
   motor.move_bot(10)  # turn right, go straight
   course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
   motor.move_bot(0)  # go straight
   course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node() 
   course_nodes.change_orientation('r')
   motor.move_bot(10)  # turn right, go straight
   course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
   motor.move_bot(8)  # turn left
   course_nodes.change_orientation('l')



#better obstacle avoidance code. has not been debugged yet
     # course_nodes.change_orientation('l')
     # motor.move_bot(1)  # turn left, go straight
    #  course_nodes.current_node = course_nodes.current_node + course_nodes.increment_node()
    #  course_nodes.change_orientation('r')
   # while course_nodes.avoidingObstacle == True:
          #irValues = sendAndReceiveValue('b', 'z', 'z')
      #   direction = course_nodes.obstacleAvoidance('e', irValues, startNode)
          # motor.move_bot(direction)
       #  time.sleep(3)
       
       # motor.move_bot('a') #turn robot left to reorient robot

      #course_nodes.change_orientation('l') #reorient direction in node
      #print ("end of obstacle avoidance**********")



#convert a character to a number to send or receive
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

#convert a number to a character to send or receive
def char2Number(number):
   if number == '1':
      return 1
   elif number == '2':
      return 2
   elif number == '3':
      return 3
   elif number == '4':
      return 4
   elif number == '5':
      return 5
   elif number == '6':
      return 6
   elif number == '7':
      return 7
   elif number == '8':
      return 8
   elif number == '9':
      return 9
   else:
      return 0


#a: see if object is in front of the robot
#b: see if object isto the right of, in front of, or left of the robot
#c: send LED value
#d: send value for seven segment display
#g: get header values

def sendAndReceiveValue(actionCode, actionToTake, color):
    
    send = actionCode
    values = ''


    if actionCode == 'a':    #see if obstacle is in front of robot
           send += '\n'
           ser.write(send)
           waitForSerial()
           values = ser.read()  #see if obstacle is to the right of, in front of, or to the left of the robot
    elif actionCode == 'b':
           send += '\n'
           ser.write(send)
          # waitForSerial()
           if ser.readline() > 0:
              sensor1 = ser.read() #right
              sensor2 = ser.read() #front
              sensor3 = ser.read() #left
           values = {1: sensor1, 2: sensor2, 3: sensor3}
    elif actionCode == 'c':  #send value and color to matrix display 
           if actionToTake < 10:
              #print (actionToTake)
              send += '0'
              send += number2Char(actionToTake)
              send += color
              send += '\n'
              ser.write(send)
           else:
              send += number2Char(math.floor(actionToTake / 10))
              send += number2Char(actionToTake % 10)
              send += color
              send += '\n'
              ser.write(send)
    elif actionCode == 'd':  #send value to 7 segment LED to display
           send += number2Char(actionToTake)
           send += '\n'
           ser.write(send)
           waitForSerial()
           values = ser.read()
    elif actionCode == 'g':
           send += '\n'
           ser.write(send)
          #ser.flush()
           if ser.readline() > 0:
              value1 = ser.read()
              value2 = ser.read()
              value3 = ser.read()              
           #waitForSerial()
             # values = ser.read()
           #ser.flush()
         #  print ("values: ", values)
           #value1 = ser.read() #right
         #  value2 = ser.read() #front
          # value3 = ser.read() #left
          # print("Values: ", values)
           print("value1", value1)
           print("value2", value2)
           print("value3", value3)

           values = char2Number(value1)*100 + char2Number(value2)*10 + char2Number(value3) #returns 3 digit integer
    else:
           send += actionCode

    #print (send)
    return values

def waitForSerial():
      serWaitCount=0
      while True:
         if (len ( ser.readline()) == 0):
            print("serial is ready. ")
            break
         elif (serWaitCount > 10000):
            print("serial timed out. ")
            break
         else:
            serWaitCount=serWaitCount+1


#after all nodes have been travsersed, this code will check to see if the unmarked nodes are above an EMF field
def completeGrid():
   for i in range(course_nodes.number_of_nodes):
      if course_nodes[i].is_perimeter == false and course_nodes[i].node_type == 'u':
         if course_nodes[i+1].is_emf == True:
            if course_nodes[i-1].is_emf == True or course_nodes[i-7].is_emf == True or course_nodes[i+7].is_emf == True:
               course_nodes[i].node_type == 'e'
               sendAndReceiveValue('c', course_nodes.current_node, color)
         elif course_nodes[i-1].is_emf == True:
            if course_nodes[i-7].is_emf == True or course_nodes[i+7].is_emf == True:
               course_nodes[i].node_type == 'e'
               sendAndReceiveValue('c', course_nodes.current_node, color)
         elif course_nodes[i+7].is_emf == True and course_nodes[i-7].is_emf == True:
               course_nodes[i].node_type == 'e'
               sendAndReceiveValue('c', course_nodes.current_node, color)

def turn(turnDirection):

   tolerance = 5
   
   if turnDirection == 'l':
      destinationHeading = -90

   elif turnDirection == 'r':
      destinationHeading = 90

   heading = sendAndReceiveValue('g', 'z', 'z') - destinationHeading
   if heading > 180:
      heading = heading - 360

   #while (abs(heading - destinationHeading) > tolerance):

def calc_motor_degree():
   destination_heading = 90;
   tolerance = 5;
   wheel_track = 5.4;
   wheel_circ = 7;
   if abs(heading) > (destination_heading + tolerance) or abs(heading) < (destination_heading - tolerance):
       theta = heading - nominal;
       theta = math.radians(theta);
       opp = (wheel_track/2)*(math.sin(theta));
       wheel_rotate = opp/wheel_circ;
       wheel_rotate = math.degrees(wheel_rotate);
   else:
         wheel_rotate = 0;
   return wheel_rotate
      

def main():
#   number_of_nodes = 50
#   course_nodes = grid.Grid(number_of_nodes)
   
#   time.sleep(4) #need this always before code begins! 4 seems to work okay


#tester. delete
  # while stillTurning != 'g':
   #   motor.movement(5,-1,100,100) #left turn
    #  stillTurning = sendAndReceiveValue('h', 'z', 'z')
    #  print (stillTurning)

   #obstacleAvoidance(course_nodes, motor) #tester. use only in grid search code

   #use for reference. do not actually include in code
    #print (course_nodes.current_node)'
    #print (course_nodes[5].is_perimeter)
    #print (course_nodes[course_nodes.current_node].is_perimeter)

       #testing
   #while stillTurning != 'g':
   #while 1:
     # motor.movement(1,-1,100,100) #left turn
    #  print (sendAndReceiveValue('g', 'z', 'z'))
    #  time.sleep(1)
      
     #call header comparison code
    #  print (stillTurning)
    #tester code
   #turn('l')

   #course_nodes.initialize()
  # PerimeterSearch(course_nodes)
  # GridSearch(course_nodes)
#
#   completeGrid()
#   time.sleep(.01)
#   print ("done")
#   while True:
#      time.sleep(.01)

   if __name__ == "__main__":
      try:
         main()
      except KeyboardInterrupt:
         GPIO.cleanup()   # clean up GPIO on CTRL+C exit.
   GPIO.cleanup()
