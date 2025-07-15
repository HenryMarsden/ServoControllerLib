#!/usr/bin/python

import time
import math
import smbus

# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:

  # Registers/etc.
  __SUBADR1            = 0x02
  __SUBADR2            = 0x03
  __SUBADR3            = 0x04
  __MODE1              = 0x00
  __MODE2              = 0x01
  __PRESCALE           = 0xFE
  __LED0_ON_L          = 0x06
  __LED0_ON_H          = 0x07
  __LED0_OFF_L         = 0x08
  __LED0_OFF_H         = 0x09
  __ALLLED_ON_L        = 0xFA
  __ALLLED_ON_H        = 0xFB
  __ALLLED_OFF_L       = 0xFC
  __ALLLED_OFF_H       = 0xFD
  


  def __init__(self, address=0x40, debug=False):
    self.bus = smbus.SMBus(1)
    self.address = address
    self.debug = debug
    if (self.debug):
      print("Reseting PCA9685")
    self.write(self.__MODE1, 0x00)
    time.sleep(.1)
    
    self.setInitialPosition()
    
    time.sleep(.5)
    
  def setInitialPosition(self):
      
    servo_pos_file = open("servo_values.txt", "r")
    panTilt = servo_pos_file.readlines()
    splitPan = panTilt[0].split(':')
    self.pan = int(splitPan[1])
    splitTilt = panTilt[1].split(':')
    self.tilt = int(splitTilt[1])
    print(self.pan)
    print(self.tilt)
    
	
  def write(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    self.bus.write_byte_data(self.address, reg, value)
    if (self.debug):
      print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))
	  
  def read(self, reg):
    "Read an unsigned byte from the I2C device"
    result = self.bus.read_byte_data(self.address, reg)
    if (self.debug):
      print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
    return result
	
  def setPWMFreq(self, freq):
    "Sets the PWM frequency"
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    if (self.debug):
      print("Setting PWM frequency to %d Hz" % freq)
      print("Estimated pre-scale: %d" % prescaleval)
    prescale = math.floor(prescaleval + 0.5)
    if (self.debug):
      print("Final pre-scale: %d" % prescale)

    oldmode = self.read(self.__MODE1);
    newmode = (oldmode & 0x7F) | 0x10        # sleep
    self.write(self.__MODE1, newmode)        # go to sleep
    self.write(self.__PRESCALE, int(math.floor(prescale)))
    self.write(self.__MODE1, oldmode)
    time.sleep(0.005)
    self.write(self.__MODE1, oldmode | 0x80)
    self.write(self.__MODE2, 0x04)

  def setPWM(self, channel, on, off):
    "Sets a single PWM channel"
    self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
    self.write(self.__LED0_ON_H+4*channel, on >> 8)
    self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
    self.write(self.__LED0_OFF_H+4*channel, off >> 8)
    if (self.debug):
      print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel,on,off))
	  
  def setServoPulse(self, channel, pulse):
    "Sets the Servo Pulse,The PWM frequency must be 50HZ"
    pulse = pulse*4096/20000        #PWM frequency is 50HZ,the period is 20000us
    self.setPWM(channel, 0, int(pulse))
  
  def calibrate(self):
    self.stutterRotation(1, 90)
    self.stutterRotation(0, 0)
    time.sleep(0.5)
    self.setRotationAngle(1, 90)
    self.setRotationAngle(0, 0)
    self.pan = 90
    self.tilt = 0
    
  def adjustAngle(self, channel, Angle):
    if channel == 0:
        absAng = self.tilt + Angle
    elif channel == 1:
        absAng = self.pan + Angle
    else:
        print("Invalid channel")
    if absAng > 0 and absAng < 180:
        self.stutterRotation(channel, absAng)
    else:
        print("Angle goes out of bounds")

  # Breaks motion of servo into chunks to smooth motion
  def stutterRotation(self, channel, Angle):
    print("stuttering to ", Angle, " from ", self.tilt ,"/", self.pan)
    
    if channel == 0:
        if self.tilt <= Angle:
            
            for i in range (self.tilt, Angle + 1, 1):
                self.setRotationAngle(channel, i)
                time.sleep(.1)
        else:
            
            for i in range (self.tilt, Angle - 1, -1):
                self.setRotationAngle(channel, i)
                time.sleep(.1)
        self.tilt = Angle
        
        print(self.tilt)
            
    elif channel == 1:
        if self.pan <= Angle:
            
            for i in range (self.pan, Angle + 1,  1):
                self.setRotationAngle(channel, i)
                time.sleep(.1)
        else:
            
            for i in range ( self.pan, Angle - 1, -1):
                self.setRotationAngle(channel, i)
                time.sleep(.1)
        self.pan = Angle

        print(self.pan)
    else:
        print("Invalid Channel")
    
    servo_pos_file = open("servo_values.txt", "w")
    servo_pos_file.write(("pan:"+str(self.pan)+"\n"))
    servo_pos_file.close()
        
    servo_pos_file = open("servo_values.txt", "a")
    servo_pos_file.write(("tilt:"+str(self.tilt)))
    servo_pos_file.close()
    
  def setRotationAngle(self, channel, Angle): 
    if(Angle >= 0 and Angle <= 180):
        temp = Angle * (2000 / 180) + 501
        self.setServoPulse(channel, temp)
    else:
        print("Angle out of range")
        
        
  def start_PCA9685(self):
    self.write(self.__MODE2, 0x04)
    #Just restore the stopped state that should be set for exit_PCA9685
    
  def exit_PCA9685(self):
    self.write(self.__MODE2, 0x00)#Please use initialization or __MODE2 =0x04

