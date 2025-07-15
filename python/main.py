#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from PCA9685 import PCA9685

class testClass():
    def setAng(self, channel, angle):
        pwm = PCA9685()
        pwm.setPWMFreq(50)
        pwm.stutterRotation(channel, angle)
    
    def mov(self, channel, angle):
        pwm = PCA9685()
        pwm.setPWMFreq(50)
        pwm.adjustAngle(channel, angle)
       
    def init(self):
        pwm = PCA9685()
        print(pwm.read(0x06))
        print(pwm.read(0x07))
        print(pwm.read(0x08))
        print(pwm.read(0x09))
    
    def calibrate(self):
        pwm = PCA9685()
        pwm.setPWMFreq(50)
        pwm.calibrate()
        

testClass = testClass()
#testClass.calibrate()
testClass.mov(1, -10)
#testClass.setAng(1, 0)