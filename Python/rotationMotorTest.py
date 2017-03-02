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


#
def movement(motors, leftMotor, rightMotor, i, j, power1, power2):
    result = BrickPiUpdateValues()
    if not result:  # if updating values succeeded
        print("=============")
        encoderStartLeft = BrickPi.Encoder[leftMotor]
        encoderStartRight = BrickPi.Encoder[rightMotor]
        print("Encoder Value: " + str(encoderStartLeft) + ' ' + str(encoderStartRight))  # print the encoder raw
        power = [power1, power2]  # 0 to 255
        deg = [i, j]
        # maxWheelSpeedDiff = motorRotateDegree (power, deg, motors, sampling_time=0.0) #to use BrickPi's version
        maxWheelSpeedDiff = motorRotateDeg(power, deg, motors,
                                           sampling_time=0.0)  # to use MultiMotorDriving's super version
        encoderEndLeft = BrickPi.Encoder[leftMotor]
        encoderEndRight = BrickPi.Encoder[rightMotor]
        deltaLeft = abs(encoderEndLeft - encoderStartLeft) // 2
        deltaRight = abs(encoderEndRight - encoderStartRight) // 2
        #       print ("Encoder Value: " + str(encoderEndLeft) + ' ' + str(encoderEndRight))	# print the encoder raw
        #       print ("Delta Value: %d %d" % (deltaLeft, deltaRight))
        #       print ("Accuracy: %d %% %d %%" % (deltaLeft * 100 // abs(deg[0]), deltaRight * 100 // abs(deg[1])))
        #       print ("Max wheel speed differential in encoder tics: %d" % maxWheelSpeedDiff)
        print("=============")
        BrickPiSense()


# Move Forward
def fwd(motors, leftMotor, rightMotor):
    # BrickPi.motorRotateDegree([200,200][1060,1060][PORT_B,PORT_C])
    movement(motors, leftMotor, rightMotor, 630, 630, 100, 100)


# Move Left
def left(motors, leftMotor, rightMotor):
    # BrickPi.motorRotateDegree([200][477][PORT_B])
    movement(motors, leftMotor, rightMotor, -187, 187, 100, 100)


def leftP(motors, leftMotor, rightMotor):
    movement(motors, leftMotor, rightMotor, -375, 0, 100, 100)


# left arc
def leftArc(motors, leftMotor, rightMotor):
    movement(motors, leftMotor, rightMotor, 315, 315, 100, 100)
    movement(motors, leftMotor, rightMotor, -90, 90, 100, 100)
    movement(motors, leftMotor, rightMotor, 477, 477, 100, 100)
    movement(motors, leftMotor, rightMotor, -90, 90, 100, 100)
    movement(motors, leftMotor, rightMotor, 315, 315, 100, 100)


# Move Right
def right(motors, leftMotor, rightMotor):
    movement(motors, leftMotor, rightMotor, 187, -187, 100, 100)


# Right Pivot
def rightP(motors, leftMotor, rightMotor):
    movement(motors, leftMotor, rightMotor, 0, -375, 100, 100)


# Slow Right
def rightS(motors, leftMotor, rightMotor):


# right arc
def rightArc(motors, leftMotor, rightMotor):
    movement(motors, leftMotor, rightMotor, 315, 315, 100, 100)
    movement(motors, leftMotor, rightMotor, 92, -92, 100, 100)
    movement(motors, leftMotor, rightMotor, 477, 477, 100, 100)
    movement(motors, leftMotor, rightMotor, 92, -92, 100, 100)
    movement(motors, leftMotor, rightMotor, 315, 315, 100, 100)


# Move backward
def back(motors, leftMotor, rightMotor):
    movement(motors, leftMotor, rightMotor, -630, -630, 100, 100)


# Stop
def stop(motors, leftMotor, rightMotor):
    movement(motors, leftMotor, rightMotor, 0, 0, 100, 100)


# Move the simplebot depending on the command
def move_bot(motors, leftMotor, rightMotor, val):
    global cmd
    if val == 'w':
        # cmd=='w'
        fwd(motors, leftMotor, rightMotor)
    elif val == 'a':
        #    cmd='a'
        left(motors, leftMotor, rightMotor)
    elif val == 'd':
        # cmd='d'
        right(motors, leftMotor, rightMotor)
    elif val == 'q':
        # cmd='q'
        leftP(motors, leftMotor, rightMotor)
    elif val == 'e':
        # cmd='e'
        rightP(motors, leftMotor, rightMotor)
    elif val == 'z':
        # cmd='z'
        leftS(motors, leftMotor, rightMotor)
    elif val == 'c':
        # cmd='c'
        rightS(motors, leftMotor, rightMotor)
    elif val == 'r':
        # cmd='c'
        leftArc(motors, leftMotor, rightMotor)
    elif val == 't':
        # cmd='c'
        rightArc(motors, leftMotor, rightMotor)
    elif val == 's':
        # cmd='s'
        stop(motors, leftMotor, rightMotor)
    elif val == 'x':
        # cmd='x'
        back(motors, leftMotor, rightMotor)

"""
def main():
    BrickPiSetup()  # Setup the serial port for communication (***NB*** APP MUST BE RUN IN SUDO MODE ***NB***)
    leftMotor = PORT_B
    rightMotor = PORT_A
    motors = [leftMotor, rightMotor]
    BrickPi.MotorEnable[leftMotor] = 1  # Don't turn these off - set its speed to 0 to stop a motor
    BrickPi.MotorEnable[rightMotor] = 1
    BrickPiSetupSensors()  # Send the properties of sensors to BrickPi
    BrickPi.Timeout = 30000  # So motors won't stop cause of lack of contact (30 seconds)
    BrickPiSetTimeout()  # (BrickPi's default is 250 msec (really meeses with motor reliability))

    while 1:
        inp = str(raw_input())  # Take input from the terminal
        move_bot(motors, leftMotor, rightMotor, inp)  # Send command to move the bot

        time.sleep(.01)  # sleep for 10 ms

if __name__ == "__main__":
    main()
"""