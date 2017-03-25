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
from BrickPi import * 				#import BrickPi.py file to use BrickPi operations
from MultiMotorDriving import * 	#So can do precision motor rotations


BrickPiSetup()  	#Setup the serial port for communication (***NB*** APP MUST BE RUN IN SUDO MODE ***NB***)
ArmMotor = PORT_C
motors = [ArmMotor]
BrickPi.MotorEnable[ArmMotor] = 1	#Don't turn these off - set its speed to 0 to stop a motor
BrickPiSetupSensors()       		#Send the properties of sensors to BrickPi
BrickPi.Timeout = 30000     		#So motors won't stop cause of lack of contact (30 seconds)
BrickPiSetTimeout()				# (BrickPi's default is 250 msec (really meeses with motor reliability))

while True:
    print ("Input is in degrees! Enter the degrees to move, or 0 to reset the encoders.")
    if p_version==2: i = int(raw_input())
    else: i = int(input())
    if i == 0:
        zeroEncoders()
        continue
    result = BrickPiUpdateValues() 
    if not result :					# if updating values succeeded
        print ("=============")
        encoderStartArm = BrickPi.Encoder[ArmMotor]
        print ( "Encoder Value: " + str(encoderStartArm))	# print the encoder raw 
        power=[100] # 0 to 255
        deg = [i]
        encoderEndArm = BrickPi.Encoder[ArmMotor]
        deltaArm = abs(encoderEndArm - encoderStartArm) // 2
        #print ("Encoder Value: " + str(encoderEndArm))	# print the encoder raw
        #print ("Accuracy: %d %% %d %%" % (deltaArm * 100 // abs(deg[0]), ))
        #print ("=============")
        BrickPiSense()
