Python document contains code to be placed on raspberry pi.
The time.sleep(x) value will need changing in the script if the time between intervals of movement need changing.
To run the code open the TestScript file in the Thonny editor and press Run at the top.
Ensure that you calibrate after powering up servo, and between tests.
To switch between calibration and testing comment out the command you do not want to run. Its best not to run both commands at once as it has not been tested, do 1 at a time for certainty.

DataConverterScript is to be placed in the same directory as the Iris output .csv files. 
The values in the script will need changing if:
  A different sensor is placed on the servos that has a different height (change "radius"),
  The source position is changed relative to the sensor (change "distance"),
  The Iris data capture rate is changed from the tested 1 capture per 10s (change "dataPointsPerRotation").
Ensure nescassary modules are installed (os, glob, math, csv).

To run complete test, set up Iris and press "Run" on the TestScript.py file inside the Thonny editor on the Pi then press start on Iris. it is currently set up to capture 6 data points (1 every 10s) and then move, if this is changed update the values as needed inside Iris and inside TestScript.py. Ensure the value inside the sleep in TestScript.py is a multiple of the value of data capture in Iris (- 0.5 to account for servo move time). The DataConverterScript.py would also needed to be changed to reflect this change by adjusting the "dataPointsPerRotation" variable to be equal to the number of data points that are to be captured between servo movements.

On RaspberryPi ensure I2C is enabled in "raspi-config".
Ensure Pi hat is powered through the external powersupply.
Follow instuctions for BCM2835 install in the docs at https://www.waveshare.com/wiki/Pan-Tilt_HAT.
If any issues are encountered consult the docs.
