#!/usr/bin/env python

'''
# This is an example of controlling the rotation of motors using encoders
# BrickPi's first Arduino runs motor ports A & b, as well as sensor ports 1 & 2. Arduino 2 does the rest of them.
# You may get better performance (certainly fewer communication errors with the BrickPi, and less work using my version
#   of the BrickPi.py driver) if you place all your motors and sensors on the same Arduino (if possible).
# My version of BrickPi.py won't bother to poll (triggered by BrickPi.UpdateValues()) an Arduino without gear.
'''

from __future__ import print_function
from __future__ import division

import time
from BrickPi import *  # import BrickPi.py file to use BrickPi operations
from MultiMotorDriving import *  # So can do precision motor rotations
#from main6 import sendAndReceiveValue# as sendAndReceiveValue
#from main6 import *


global delta_heading
global updated_heading
global initial_heading

#delta_heading = get_delta_heading()
#updated_heading = get_updated_heading()
#initial_heading = get_initial_heading()


class MotorControls:


    #initialization function
    def __init__(self, left_motor, right_motor):
        BrickPiSetup()  # Setup the serial port for communication (***NB*** APP MUST BE RUN IN SUDO MODE ***NB***)
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.motors = [left_motor, right_motor]
        BrickPi.MotorEnable[left_motor] = 1  # Don't turn these off - set its speed to 0 to stop a motor
        BrickPi.MotorEnable[right_motor] = 1
        BrickPiSetupSensors()  # Send the properties of sensors to BrickPi
        BrickPi.Timeout = 30000  # So motors won't stop cause of lack of contact (30 seconds)
        BrickPiSetTimeout()  # (BrickPi's default is 250 msec (really meeses with motor reliability))

    #
    def movement(self, i, j, power1, power2):
        result = BrickPiUpdateValues()
        if not result:  # if updating values succeeded
            print("=============")
            encoderStartLeft = BrickPi.Encoder[self.left_motor]
            encoderStartRight = BrickPi.Encoder[self.right_motor]
            print("Encoder Value: " + str(encoderStartLeft) + ' ' + str(encoderStartRight))  # print the encoder raw
            power = [power1, power2]  # 0 to 255
            deg = [i, j]
            # maxWheelSpeedDiff = motorRotateDegree (power, deg, motors, sampling_time=0.0) #to use BrickPi's version
            maxWheelSpeedDiff = motorRotateDeg(power, deg, self.motors,
                                               sampling_time=0.0)  # to use MultiMotorDriving's super version
            encoderEndLeft = BrickPi.Encoder[self.left_motor]
            encoderEndRight = BrickPi.Encoder[self.right_motor]
            deltaLeft = abs(encoderEndLeft - encoderStartLeft) // 2
            deltaRight = abs(encoderEndRight - encoderStartRight) // 2
            #       print ("Encoder Value: " + str(encoderEndLeft) + ' ' + str(encoderEndRight))	# print the encoder raw
            #       print ("Delta Value: %d %d" % (deltaLeft, deltaRight))
            #       print ("Accuracy: %d %% %d %%" % (deltaLeft * 100 // abs(deg[0]), deltaRight * 100 // abs(deg[1])))
            #       print ("Max wheel speed differential in encoder tics: %d" % maxWheelSpeedDiff)
           ## print("=============")
           # BrickPiSense()

  # Move Forward
    def fwd(self):
        # BrickPi.motorRotateDegree([200,200][1060,1060][PORT_B,PORT_C])
        self.movement(630, 630, 100, 100)


    # Move Left
    def left(self):
        # BrickPi.motorRotateDegree([200][477][PORT_B])
        self.movement(-187, 187, 100, 100)


    def leftP(self):
        self.movement(-375, 0, 100, 100)


    # left arc
    def leftArc(self):
        self.movement(315, 315, 100, 100)
        self.movement(-90, 90, 100, 100)
        self.movement(477, 477, 100, 100)
        self.movement(-90, 90, 100, 100)
        self.movement(315, 315, 100, 100)


    # Move Right
    def right(self):
        self.movement(187, -187, 100, 100)


    # Right Pivot
    def rightP(self):
        self.movement(0, -375, 100, 100)


    # Slow Right
    def rightS(self): {}


    # right arc
    def rightArc(self):
        self.movement(315, 315, 100, 100)
        self.movement(92, -92, 100, 100)
        self.movement(477, 477, 100, 100)
        self.movement(92, -92, 100, 100)
        self.movement(315, 315, 100, 100)

    # half right arc
    def rightHalfArc1(self):
        self.movement(315, 315, 100, 100)
        self.movement(92, -92, 100, 100)
        self.movement(238, 238, 100, 100)

    # half right arc
    def rightHalfArc2(self):
        self.movement(238, 238, 100, 100)
        self.movement(92, -92, 100, 100)
        self.movement(315, 315, 100, 100)
        
    # half right arc
    def leftHalfArc1(self):
        self.movement(315, 315, 100, 100)
        self.movement(-92, 92, 100, 100)
        self.movement(238, 238, 100, 100)

    # half right arc
    def leftHalfArc2(self):
        self.movement(238, 238, 100, 100)
        self.movement(-92, 92, 100, 100)
        self.movement(315, 315, 100, 100)
        
    # Move backward
    def back(self):
        self.movement(-630, -630, 100, 100)

    # Stop
    def stop(self):
        self.movement(0, 0, 100, 100)

    #turn left, then go straight
    def leftStraight(self):
        self.left()
        #self.stop()
        self.fwd()

    #turn left, then go straight
    def straightLeft(self):
        self.fwd()
       # self.stop()
        self.left()

    #turn left, then go straight
    def straightRight(self):
        self.fwd()
       # self.stop()
        self.right()

    #turn left, straight, left
    def leftStraightLeft(self):
        self.leftStraight()
        self.left()

    #turn right, then go straight
    def rightStraight(self):
        self.right()
       # self.stop()
        self.fwd()

    #turn right, go straight, turn right
    def rightStraightRight(self):
        self.rightStraight()
        self.right()

    def fullTurn(self):
        self.right()
        self.right()

    # Move according to the command
    def move_bot(self,val):
        global cmd
        if val == 'w':
            # cmd=='w'
            self.go_forward
##        elif val == 6:
##            #self.straightLeft()
##            #self.fwd()
##            #self.go_forward
##            self.left()
##            #self.go_left
        elif val == '.':
            #self.straightLeft()
            #self.fwd()
            #self.left()
            #self.go_forward
            self.go_left
##        elif val == 5:
##            #self.straightRight()
##            self.fwd()
##            #self.go_forward
##            self.right()
##            #self.go_right
        elif val == 'v':
            #self.straightRight()
            #self.fwd()
            #self.right()
            #self.go_forward
            self.go_right
        elif val == 'a':
            #    cmd='a'
            self.left()
        elif val == 'd':
            # cmd='d'
            self.right()
        elif val == 'q':
            # cmd='q'
            self.leftP()
        elif val == 'e':
            # cmd='e'
            self.rightP()
        elif val == 'z':
            # cmd='z'
            self.leftS()
        elif val == 'c':
            # cmd='c'
            self.rightS()
        elif val=='h':
                #cmd='c'
            self.rightHalfArc1()
        elif val=='j':
                #cmd='c'
            self.rightHalfArc2()
        elif val=='n':
                #cmd='c'
            self.leftHalfArc1()
        elif val=='m':
                #cmd='c'
            self.leftHalfArc2()
        elif val == 'r':
            # cmd='c'
            self.leftArc()
        elif val == 't':
            # cmd='c'
            self.rightArc()
        elif val == 's':
            # cmd='s'
            self.stop()
        elif val == 'x':
            # cmd='x'
            self.back()
        elif val == 'l':
            #cmd = 'l'
            self.leftIMU()
        elif val == 'p':
            #cmd = 'l'
            self.rightIMU()
      

    '''def move_bot(self,val):
        global cmd
        if val == 0:
            #cmd=='w'
            self.fwd()
        elif val == 8:
            #cmd='a'
            self.left()
        elif val == 7:
            #cmd='d'
            self.right()
        elif val == 'q':
            #cmd='q'
            self.leftP()
        elif val == 'e':
            #cmd='e'
            self.rightP()
        elif val == 'z':
            #cmd='z'
            self.leftS()
        elif val == 'c':
            # cmd='c'
            self.rightS()
        #elif val=='h':
                #cmd='c'
            self.rightHalfArc1()
        #elif val=='j':
                #cmd='c'
            self.rightHalfArc2()
        #elif val=='n':
                #cmd='c'
            self.leftHalfArc1()
        #elif val=='m':
                #cmd='c'
            self.leftHalfArc2()
        #elif val == 'r':
            # cmd='c'
            self.leftArc()
        #elif val == 't':
            # cmd='c'
            self.rightArc()
        elif val == 4:
            # cmd='s'
             self.stop()
        #elif val == 'x':
            # cmd='x'
            self.back()
        elif val == 1:
            #cmd = 'l'
            self.leftStraight()
        elif val == 10:
            #cmd = 'l'
            self.rightStraight()
        elif val == 'n':
            self.leftStraightLeft()
        elif val == 'b':
            self.rightStraightRight()
        elif val == 9:
            self.fullTurn()
        elif val == 5:
            self.straightRight()
        elif val == 6:
            self.straightLeft()'''

#get_initial_heading(heading)
#get_updated_heading(heading)
#get_delta_heading



# IMU functions  ********************************************************

    def get_initial_heading():
        heading=sendAndReceiveValue('h','z','z')
        if heading > 180:
            initial_heading = heading - 360;
        else:
            initial_heading = heading;
        return initial_heading

    def get_updated_heading():
        heading=sendAndReceiveValue('h','z','z')
        if heading > 180:
          updated_heading = heading - 360;
        else:
          updated_heading = heading;
        return updated_heading

    def get_delta_heading(initial_heading,updated_heading):
        delta_heading = updated_heading - initial_heading;
        return delta_heading

# Straight move********************************************************
    def go_forward():
        upper_limit = 5;
        lower_limit = -5;
        get_initial_heading()
        fwd()
        get_updated_heading()
        get_delta_heading()
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
    def go_right():
        # correct heading while turning right
        upper_limit = 95;
        lower_limit = 85;
        get_initial_heading()
        self.right()
        get_updated_heading()
        get_delta_heading()

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
    def go_left():
        # correct heading while turning right
        upper_limit = -95;
        lower_limit = -85;
        get_initial_heading()
        self.left()
        get_updated_heading()
        get_delta_heading()
        
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



#initialize motor
left_motor = PORT_B
right_motor = PORT_A
motor = MotorControls(left_motor, right_motor)
#move_bot.self('w')

#motor.right()
#while 1:
   # time.sleep(1)
