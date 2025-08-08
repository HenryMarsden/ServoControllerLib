import csv
import math as maths
import glob
import os
    
dataPointsPerRotation = 6 
   
def calcInvSqu(itteration):
    radius = 2.85 # Change if new board placed on servo - measure distance from tilt servo hinge to the sensor
    distance = 9.75 # Change if source moved in relation to the board - measure distance from source centre to sensor
    intConv = (itteration)/dataPointsPerRotation # Compensates for increment of loop
    angleConv = (intConv) * 5 # Quantizes the angle into 5 degree increments
    radAngle = maths.radians(angleConv)
    distanceInc = radius * (1 - maths.cos(radAngle))
    dropOff = 1/pow(distance + distanceInc, 2)
    return dropOff

def averageValues(placement, quantity, numSet):
    avg = 0
    for i in range(placement, placement-quantity, -1):
        avg = avg + (int(numSet[i])/quantity)
    return avg

def main():
    # Types of headers for the Iris data varieties - used to automatically detect data type
    n3sHeaders = ['DateTime', ' Status', ' Real Time', 'HDS Counts', ' HDS Dose', ' HDS Dose Rate', ' HDS Live Time', ' HDS Leakage CurrentVHDS Counts', ' VHDS Dose', ' VHDS Dose Rate', ' VHDS Live Time', 'Combined Dose Rate', ' Current Dose Sensor', 'CZT Counts', ' CZT Dose', ' CZT Dose Rate', ' CZT Live Time', 'CZT Bias', 'Sealicon Raw', ' Sealicon Total Dose', ' Sealicon Sensor SelectedDetector TemperatureCZT Dropped Counts', ' HDS Dropped Counts', ' VHDS Dropped Counts', ' Vibration Counts', '  Accelerometer Maximum ValueSpectrum Bits', 'Spectrum Bins']
    aqHeaders = ['DateTime', 'Status', 'Real Time', 'HDS 1 Counts', 'HDS 1 Dose', 'HDS 1 Dose Rate', 'HDS 1 Current ADC', 'HDS 2 Counts', 'HDS 2 Dose', 'HDS 2 Dose Rate', 'HDS 2 Current ADC', 'ADS 1 Dose', 'ADS 1 DoseRate', 'ADS 1 Current ADC', 'ADS 2 Dose', 'ADS 2 DoseRate', 'ADS 2 Current ADC', 'Neutron Live Time', 'Neutron Counts', 'Neutron Temperature', 'Neutron Current ADC', 'Gamma Live Time', 'Gamma Counts', 'Gamma Dose', 'Gamma Temperature', 'Gamma Current ADC', 'Spectrum Bits', 'Spectrum Bins']
    
    # Finds headers of the file to compare to above header arrays
    list_of_files = glob.glob('*.csv') # * means all if need specific format then *.csv
    file_path = max(list_of_files, key=os.path.getctime)
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
    
    if headers == aqHeaders:
        c2Str = 'Gamma Counts'
        c1Str = 'HDS 1 Counts'
        timeStr = 'DateTime'
    elif headers == n3sHeaders:
        c2Str = ' CZT Dose'
        c1Str = 'HDS Counts'
        timeStr = 'DateTime'
    else:
        print("ERROR: invalid filetype - consider removing output.csv")
 
    # Calculate expected inverse square dropoff for distance traveled by tilt servo away from the source
    baseStrength = calcInvSqu(0)
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        row_count = sum(1 for row in reader)
        
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        c2 = [row[c2Str] for row in reader]
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        c1 = [row[c1Str] for row in reader]
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        time = [row[timeStr] for row in reader] 
    
    for i in range(0, row_count-1, dataPointsPerRotation):
        dropOff = calcInvSqu(i - dataPointsPerRotation)# -increment because the first loop is used to fill label collums so itteration is 1 increment off
        incVal = baseStrength/dropOff
        if(i == 0):
            with open("output -" +file_path+".csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([timeStr, c1Str, c2Str, c1Str + ' Normalized', c2Str + 'Normalized', 'Normalization Factor' 'Angle'])
        else:
            with open("output -"+file_path+".csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                c1Avg = round(averageValues(i, dataPointsPerRotation, c1),2)
                c2Avg = round(averageValues(i, dataPointsPerRotation, c2),2)
                c1AvgNorm = round(averageValues(i, dataPointsPerRotation, c1)*incVal,2)
                c2AvgNorm = round(averageValues(i, dataPointsPerRotation, c2)*incVal, 2)
                writer.writerow([time[i], c1Avg, c2Avg, c1AvgNorm, c2AvgNorm, round(incVal, 2), 5 * (i/dataPointsPerRotation - 1)])

if __name__ == "__main__":
    main()
    print("results in output - filename.txt")
    input()
