import pandas as pd
import numpy as np
import csv
import math as maths

    
def calcInvSqu(itteration):
    intConv = (itteration + 1)/3
    angleConv = (intConv - 1) * 5
    radAngle = maths.radians(angleConv)
    distanceInc = 3.42 * (1 - maths.cos(radAngle))
    dropOff = 1/pow(15.5 + distanceInc, 2)
    return dropOff

def main():
    # Configuration
    #file_path = "D3R4012XX 2025-07-31 133045 AquilaSpectrum.csv"  # Change this to your CSV file path
    print("filename:")
    file_path = input()
    
    baseStrength = calcInvSqu(2)
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        row_count = sum(1 for row in reader)
        
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        c2 = [row['Gamma Counts'] for row in reader]
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        c1 = [row['HDS 1 Counts'] for row in reader]
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        time = [row['DateTime'] for row in reader]  # Replace 'ColumnName' with your column's name
    
    for i in range(1, row_count-1, 3):
        print(time[i],',',c1[i], ',' , c2[i],"\n")
    print("==================\n==================")
    for i in range(1, row_count-1, 3):
        dropOff = calcInvSqu(i)
        incVal = baseStrength/dropOff
        print(time[i],',',int(c1[i])*incVal, ',' , int(c2[i])*incVal, ", * ",incVal,"\n")
        if(i == 1):
            with open("output.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(['DateTime', 'HDS 1 Counts','Gamma Counts','HDS 1 Counts Normalized', 'Gamma Counts Normalized', 'Normalization Factor'])
        else:
            with open("output.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([time[i],int(c1[i]),int(c2[i]),int(c1[i])*incVal,int(c2[i])*incVal,incVal])

if __name__ == "__main__":
    main()
    print("results in output.txt")
    input()
