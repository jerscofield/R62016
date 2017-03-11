from __future__ import print_function
from __future__ import division
from binascii import hexlify

import grid
#import rotationMotorTest
import serial

import time
#from BrickPi import *  # import BrickPi.py file to use BrickPi operations
#from MultiMotorDriving import *  # So can do precision motor rotations


def main():
    number_of_nodes = 49

    course_nodes = grid.Grid(number_of_nodes)
    course_nodes.is_searching = 1
    #left_motor = PORT_B
   # right_motor = PORT_A
   # motor = rotationMotorTest.MotorControls(left_motor, right_motor)  

    ser = serial.Serial('/dev/ttyACM0',9600)
    has_been_pressed = 0
    while has_been_pressed == 0:
        read_serial=ser.read()
        if (read_serial == '1'):
            has_been_pressed = 1

#    time.sleep(1)
   #  BrickPiSetup()  # Setup the serial port for communication (***NB*** APP MUST BE RUN IN SUDO MODE ***NB***)
   #  self.leftMotor = PORT_B
   #  self.rightMotor = PORT_A
   #  self.motors = [leftMotor, rightMotor]
   # BrickPi.MotorEnable[leftMotor] = 1  # Don't turn these off - set its speed to 0 to stop a motor
   # BrickPi.MotorEnable[rightMotor] = 1
   # BrickPiSetupSensors()  # Send the properties of sensors to BrickPi
   # BrickPi.Timeout = 30000  # So motors won't stop cause of lack of contact (30 seconds)
   # BrickPiSetTimeout()  # (BrickPi's default is 250 msec (really meeses with motor reliability))

    #call motor object for controling the motor
    #perimeter search. will continue to run as long as the last node hasn't been reached
    while course_nodes.is_searching == 1:
        print ("Your current node is: ", course_nodes.current_node)
        action_to_take = course_nodes.next_node()

        #signal to the arduino that the pi is ready to get input
        ser.write('g');
        print ("Serial has been sent to the Arduino!")
        
     #   for i in range(2):
        EMF = ser.read()
        ir_sensor = ser.read()
        print (EMF)
        print (ir_sensor)        

        #save to nodes  
        if action_to_take == 0:
            inp = 'w'       #robot isn't at a corner. go straight.
        elif action_to_take == 2:
            inp = 'n'       #robot is right before the corner. does a half turn onto the corner
        elif action_to_take == 1:
            inp = 'm'       #robot is at a corner. does a half turn onto the next node

       # motor.move_bot(inp)  # Send command to move the bot
        print (action_to_take)
        time.sleep(1)  # sleep for 10 ms

    ser.write('d')
    print ("Done with perimeter search!")
    while 1:
        time.sleep(.01)

if __name__ == "__main__":
    main()

    """
    def main():
        number_of_nodes = 49
        course_nodes = grid.Grid(number_of_nodes)
        course_nodes.search_perimeter()

        for i in range(number_of_nodes):
            print (course_nodes[i].node_number)

    if __name__ == "__main__":
        main()
       """