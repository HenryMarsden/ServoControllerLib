from PCA9685 import PCA9685
import time

class TestScript:
  pwm = None
  
  def __init__(self):
    self.pwm = PCA9685()
    self.pwm.setPWMFreq(50)
    
  def tilt(self, rang, incr):
    self.calibrate()
    for i in range(6, rang + 2, incr):
      self.pwm.stutterRotation(0, i)
      print(self.calcDropOff())
      time.sleep(59.5) # Change value for time between rotations, ensure it is a multiple of the Iris data capture time window

  def calibrate(self):
    self.pwm.calibrate()

  def calcDropOff(self):
    radius = 2.85
    distance 9.75
    return self.pwm.calcInvSqu(distance, radius)

# calibrate between and before every test. Uncomment lines as needed.
ts = TestScript()
#ts.tilt(80, 5) 
ts.calibrate()
