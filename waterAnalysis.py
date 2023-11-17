# Program takes input and finds if data dips below the user input
# Also finds the number of events, lowest point, and duration of each event

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

with open('results.txt', 'w') as file:

    # names for columns
    columnNames = ['time', 'interval', 'temps']
    # read in csv data to analyze
    data = pd.read_csv('./wiseWaterExData.csv', names=columnNames, header=0, usecols=[0, 1, 2])

    degree = chr(176)  # char for degree symbol
    tempLimit = float(input("What is the lowest acceptable temp. in " + degree + "C?  "))
    dataLength = len(data)  # indexing starts at 0
    flagOne = False
    eventCounter = 1

    # checks for initial event
    for i in range(dataLength):
        if data.temps[i] < tempLimit:
            flagOne = True
            break

    if flagOne is True:
        # print statements for output
        print('\n\t\t\t\t\t\t\t\t\t\t\tWater Temperature Information\n', file=file)
        print('------------------------------------------------------------------------------------------------------------------------------------------------------\n', file=file)
        print('\t# of Event\t\tStart Time\t\t\t\tEnd Time\t\t\t\tLow Temp.\t\tSpike Time\t\t\t\tTotal Duration\n', file=file)
        print('------------------------------------------------------------------------------------------------------------------------------------------------------\n', file=file)
        # initializes new variables
        flagTwo = False
        startTime = 0
        endTime = 0
        # loop through data
        for i in range(dataLength):
            if data.temps[i] < tempLimit and flagTwo is False: # this indicates the start of an event
                lowPoint = 100
                startI = i
                startTime = datetime.strptime(data.time[i], "%m/%d/%Y %H:%M:%S %p") # restructures time for later
                flagTwo = True
            elif data.temps[i] >= tempLimit and flagTwo is True: # this indicates the end of an event
                endTime = datetime.strptime(data.time[i], "%m/%d/%Y %H:%M:%S %p") # restructures time for later
                endI = i
                for j in range(startI, endI): # finds low point in total event for spike
                    if data.temps[j] <= lowPoint:
                        lowPoint = data.temps[j]
                        spikeTime = datetime.strptime(data.time[j], "%m/%d/%Y %H:%M:%S %p") # restructures time for later
                totalTime = endTime - startTime
                # add lambda expression to remove small intervals, such as min of 3 minutes
                print('\t{}\t\t\t\t{}\t\t{}\t\t{}\t\t\t{}\t\t{}'.format(eventCounter, startTime, endTime, lowPoint, spikeTime, totalTime), file=file)
                eventCounter += 1
                flagTwo = False
            elif i + 1 >= dataLength and data.temps[i] < tempLimit: # this checks for edge case where last data point is included in event
                endTime = datetime.strptime(data.time[i], "%m/%d/%Y %H:%M:%S %p") # restructures time for later
                endI = i
                for j in range(startI, endI):
                    if data.temps[j] <= lowPoint:
                        lowPoint = data.temps[j]
                        spikeTime = datetime.strptime(data.time[j], "%m/%d/%Y %H:%M:%S %p") # restructures time for later
                totalTime = endTime - startTime
                # add lambda expression to remove small intervals, such as min of 3 minutes
                print('\t{}\t\t\t\t{}\t\t{}\t\t{}\t\t\t{}\t\t{}'.format(eventCounter, startTime, endTime, lowPoint, spikeTime, totalTime), file=file)
                eventCounter += 1
                flagTwo = False
        # print statements for output
        print('\nThe temperature of the water DID dip below the lowest acceptable input.', file=file)
        print('\nThe lowest limit was exceeded {} times.'.format(str(eventCounter - 1)), file=file)
    else:
        print('\nThe temperature of the water DID NOT dip below the lowest acceptable value.', file=file)

print('Results can be found in results.txt')
print('Data plot being created... may take a minute or two')

# plot creation for data
plt.scatter(data.time, data.temps)
plt.xlabel('Time in Days')
plt.ylabel('Water Temperature in degrees C')
plt.axhline(y=tempLimit, color='red', linestyle='--', label='temp. limit')
plt.title('Temperature of Water in the NRV Mall Watershed Over Time')
plt.show()