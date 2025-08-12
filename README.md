## How to control the servo motor
To move the servo the **PCA9685** library inside the python folder must be implemented, an example of which can be found in the **TestScript.py** file.
Inside the **PCA9685** class there are only two methods that should be used:
* `calibrate()` - takes no arguments, returns the servos to their base position.
* `stutterRotation(channel, angle)` - *channel* refers to the pan (represented by 0) or the tilt (1) servo and *angle* refers to the angle to be moved to.

Ensure that calibrate is called after powering up servo, and between tests. This needed because the stutterRotation function requires the position of the servos to be accurate to the values that are stored in **servo_values.txt**, which can become missaligned if the servo jutters on start up or is moved by hand.

Inside **TestScript.py** two methods have been created to implement a more complete implementation of this functionality through the commands:
* `tilt(range, increment)` - *range* represents the final angle to be moved to and *increment* referes to the size of the steps to be moved through. This command takes no channel as it only works on the tilt servo. use the `pan(range, increment)` function to control the pan servo.
* `calibrate()` - no arguments, functions simply as a wrapper to unify the nescassary commands under a single instance of the TestScript class

When using the **TestScript.py** class, if it is required to switch between calibration and testing, comment out the command you do not want to run. Its best not to run both commands at once as it has not been tested.  

The `time.sleep(x)` value will need changing inside **TestScript.py** if the time between intervals of movement need changing. **_Ensure the value for `time.sleep(x)` is a multiple of the sample rate inside Iris minus 0.5_**  

## Data Converter Script notes
The **DataConverterScript.py** find the newest .csv file inside its current directory, detects the Iris detection type, and normalizes the values retrieved from the detector by Iris based on the distance traveled by the rotating servo. The output of this will be put in a file called **output - [filename].csv**.  

To use this, **DataConverterScript.py** must be placed in the same directory as the Iris output .csv files. When the script has generated a file, said generated file must be removed from the directory, or Iris must capture more data, before the script should be used again (because the script saves needing inputs by automatically working on the newest .csv file inside its directory).  
**_Because of this time saving technique, it is reccomended that between each Iris run, the DataConverterScript.py be run_**  

The values in the script will need changing if:  
* A different sensor is placed on the servos that has a different height (change `radius`),  
* The source position is changed relative to the sensor (change `distance`),  
* The Iris data capture rate is changed from the tested 1 capture per 10s (change `dataPointsPerRotation`).  
Ensure nescassary modules are installed (os, glob, math, csv).  


## How to run a complete test: 
set up Iris, then press "Run" on the TestScript.py file inside the Thonny editor on the Pi, then press start on Iris within 5 seconds. It is currently set up to capture 6 data points (1 every 10s) between servo movements, if this is changed update the values as required inside Iris and inside TestScript.py. Ensure the value inside the sleep in TestScript.py is a multiple of the value of data capture in Iris (- 0.5 to account for servo move time). The DataConverterScript.py would also needed to be changed to reflect this change by adjusting the "dataPointsPerRotation" variable to be equal to the number of data points that are to be captured between servo movements.

## Pi setup (if Pi needs to be reset)
* Ensure I2C is enabled in "raspi-config".   
* Ensure Pi hat is powered through the external powersupply.  
* Follow instuctions for BCM2835 install in the docs at https://www.waveshare.com/wiki/Pan-Tilt_HAT.  
* If any issues are encountered consult the docs.  
