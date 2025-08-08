Python document contains code to be placed on raspberry pi
The time.sleep(x) value will need chaning in the script if the time between intervals of movement need changing

DataConverterScript is to be placed in the same directory as the Iris output .csv files. 
The values in the script will need changing if:
  A different sensor is placed on the servos that has a different height (change "radius")
  The source position is changed relative to the sensor (change "distance")
  The Iris data capture rate is changed from the tested 1 capture per 10s (change "dataPointsPerRotation")

On RaspberryPi ensure I2C is enabled in "raspi-config"
Ensure Pi hat is powered through the external powersupply
Follow instuctions for BCM2835 install in the docs at https://www.waveshare.com/wiki/Pan-Tilt_HAT
If any issues are encountered consult the docs
