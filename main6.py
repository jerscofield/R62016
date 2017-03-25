# Main Robot Code
# UMKC SCE Senior Design Project
# Team R6
# Marjorie Castro, Gretchen Gilbreath, Eric Jackson, Jeremy Scofield, Katy Struthers.
# Spring 2017

# Rigoberto


# Import ******************************************************************
from __future__ import print_function
from __future__ import division

import grid
#import rotationMotorTest
from rotationMotorTest import *
import RPi.GPIO as GPIO
import serial
import time
import os

import math

number_of_nodes = 49
course_nodes = grid.Grid(number_of_nodes)
heading = 0 # init global heading variable.

#motor control
from BrickPi import *  # import BrickPi.py file to use BrickPi operations
from MultiMotorDriving import *  # So can do precision motor rotations

# Initialize Motors *******************************************************
left_motor = PORT_B
right_motor = PORT_A
motor = MotorControls(left_motor, right_motor)

#rotationMotorTest.MotorControls.__init__

ser = serial.Serial('/dev/ttyAMA0',9600, timeout = 2)  #use with arduino uno

# Buttons & Functions ****************************************************

# GREEN
def system_action(STARTBUTTON):
     print("Start Button press detected.")
     StartMain()

# RED
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

STOPBUTTON = 04
GPIO.setmode(GPIO.BCM)
GPIO.setup(04, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(STOPBUTTON, GPIO.FALLING, bouncetime = 400)
STARTBUTTON = 21
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(STARTBUTTON, GPIO.FALLING, bouncetime = 400)
         

def HaltRobot(channel):
     print ("HaltRobot button test confirmed")
     motor.move_bot('s')  # Send command to stop the bot
#     os.system.KeyboardInterrupt  #shuts down entire operating system
  
def Shutdown(channel):
     print ("Shutdown button test confirmed")
     motor.move_bot('s')  # Send command to stop the bot
     GPIO.cleanup()
     os.system("sudo shutdown -h now")  #shuts down entire operating system

def Reboot(channel):
     print ("Reboot button test confirmed")
     motor.move_bot('s')  # Send command to stop the bot
     GPIO.cleanup()
     os.system("sudo reboot")  #shuts down entire operating system

def StartMain(channel):
     print ("Start button pressed")
     motor.move_bot('s')  # Send command to stop the bot
     main()
      

# Perimeter Search **************************************************
def PerimeterSearch(course_nodes):
     course_nodes.is_searching = 1
     while course_nodes.is_searching == 1:
          course_nodes[course_nodes.current_node].traversed = 1
          sendAndReceiveValue('c', int(course_nodes.current_node), 'r')
          action_to_take = course_nodes.next_node_perim()
          if action_to_take == 0:
               inp = 'w'       # go straight unless at corner.
          elif action_to_take == 6:
               inp = '.'       # at a corner. Turn Left.
          motor.move_bot(inp)  # Send command to move the bot
          #time.sleep(1)
         
# Grid Search **********************************************************
def GridSearch(course_nodes):
     course_nodes.is_searching = 1
     while course_nodes.is_searching == 1:
          course_nodes[course_nodes.current_node].traversed = True
          print ("Grid Search", course_nodes.current_node)

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

          motor.move_bot(inp)  # Send command to move the bot
          time.sleep(.5)

# Obstacle Avoidance
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

# Integer to Character Conversion
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


def sendAndReceiveValue(actionCode, actionToTake, color):
    
     send = actionCode
     values = ' '

     #
     if actionCode == 'a':
          send += '\n'
          ser.write(send)
          values = ser.read()
     elif actionCode == 'b':
          # Read IR sensors.
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
          send += actionToTake
          send += '\n'
          ser.write(send)
     elif actionCode == 'h':
          send += '\n'
          ser.write(send)
          heading1 = ser.read()
          heading2 = ser.read()
          heading3 = ser.read()
          readHeading = heading1*100 + heading2*10 + heading3
          return readHeading
     else:
          send = actionCode
          send += actionCode

     
# IMU functions  ********************************************************

def get_initial_heading(heading):
     if heading > 180:
          initial_heading = heading - 360;
     else:
          initial_heading = heading;
     return initial_heading

def get_updated_heading(heading):
     if heading > 180:
          updated_heading = heading - 360;
     else:
          updated_heading = heading;
     return updated_heading

def get_delta_heading(initial_heading,updated_heading):
     delta_heading = updated_heading - initial_heading;
     return delta_heading

# Straight move********************************************************
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

# Right Turn********************************************************
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

# Left Turn********************************************************
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

# MAIN PROGRAM
#********************************************************
def main():
     number_of_nodes = 49
     course_nodes = grid.Grid(number_of_nodes)
     #heading=sendAndReceiveValue('h','z','z')
     #print(heading)
     #time.sleep(4)
         
     course_nodes.initialize()
     print ("Course grid initialized.")
     PerimeterSearch(course_nodes)
     print ("Perimeter Search Complete.")
     GridSearch(course_nodes)
     print ("Grid Search Complete.")

     time.sleep(.01)
     print ("done")
     while True:
          time.sleep(.01)

#********************************************************
# Run main program.
#********************************************************
#while True:
#    time.sleep(.2) 

time.sleep(10)

if __name__ == "__main__":
     try:
          main()
     except KeyboardInterrupt:
          GPIO.cleanup()   # clean up GPIO on CTRL+C exit.

GPIO.cleanup()
