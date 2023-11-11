# Program takes input and finds if data dips below the user input
# Also finds the number of events, lowest point, and duration of each event

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# names for columns
columnNames = ['time', 'interval', 'temps']
# read in csv data to analyze
data = pd.read_csv('./wiseWaterExData.csv', names=columnNames, header=0, usecols=[0, 1, 2])

degree = chr(176)  # Char for degree symbol
tempLimit = float(input("What is the lowest acceptable temp. in " + degree + "C?  "))
dataLength = len(data)  # Indexing starts at 0
flagOne = False
eventCounter = 1

# checks for initial event
for i in range(dataLength):
    if data.temps[i] < tempLimit:
        flagOne = True
        break

if flagOne is True:
    # print statements for output
    print('\n\t\t\t\t\t\t\t\tWater Temperature Information\t\t\t\t\t\n')
    print('------------------------------------------------------------------------------------------------------------------------------------------------------\n')
    print('# of Event\t\tStart Time\t\t\tEnd Time\t\t\tLow Temp.\tSpike Time\t\t\tTotal Duration\n')
    print('------------------------------------------------------------------------------------------------------------------------------------------------------\n')
    # initializes new variables
    flagTwo = False
    startTime = 0
    endTime = 0
    # loop through data
    for i in range(dataLength):
        if data.temps[i] < tempLimit and flagTwo is False:
            lowPoint = 100
            startI = i
            startTime = datetime.strptime(data.time[i], "%m/%d/%Y %H:%M:%S %p")
            flagTwo = True
        elif data.temps[i] >= tempLimit and flagTwo is True:
            endTime = datetime.strptime(data.time[i], "%m/%d/%Y %H:%M:%S %p")
            endI = i
            for j in range(startI, endI):
                if data.temps[j] <= lowPoint:
                    lowPoint = data.temps[j]
                    spikeTime = datetime.strptime(data.time[j], "%m/%d/%Y %H:%M:%S %p")
            totalTime = endTime - startTime
            # add lambda expression to remove small intervals, such as min of 3 minutes
            print('\t', eventCounter, '\t\t', startTime, '\t\t', endTime, '\t\t', lowPoint, '\t\t', spikeTime, '\t\t', totalTime)
            eventCounter += 1
            flagTwo = False
        elif i + 1 >= dataLength and data.temps[i] < tempLimit:
            endTime = datetime.strptime(data.time[i], "%m/%d/%Y %H:%M:%S %p")
            endI = i
            for j in range(startI, endI):
                if data.temps[j] <= lowPoint:
                    lowPoint = data.temps[j]
                    spikeTime = datetime.strptime(data.time[j], "%m/%d/%Y %H:%M:%S %p")
            totalTime = endTime - startTime
            # add lambda expression to remove small intervals, such as min of 3 minutes
            print('\t', eventCounter, '\t\t', startTime, '\t\t', endTime, '\t\t', lowPoint, '\t\t', spikeTime, '\t\t', totalTime)
            eventCounter += 1
            flagTwo = False
    # print statements for output
    print('\nThe temperature of the water DID dip below the lowest acceptable input.')
    print('\nThe lowest limit was exceeded ' + str(eventCounter-1) + ' times.')
    # plot here
    plt.scatter(data.time, data.temps)
    plt.xlabel('Time in Days')
    plt.ylabel('Water Temperature in degrees C')
    plt.axhline(y=tempLimit, color='red', linestyle='--', label='temp. limit')
    plt.title('Temperature of Water in the NRV Mall Watershed Over Time')
    plt.show()
else:
    print('\nThe temperature of the water DID NOT dip below the lowest acceptable value.')
    plt.scatter(data.time, data.temps)
    plt.xlabel('Time in Days')
    plt.ylabel('Water Temperature in degrees C')
    plt.axhline(y=tempLimit, color='red', linestyle='--', label='temp. limit')
    plt.title('Temperature of Water in the NRV Mall Watershed Over Time')
    plt.show()