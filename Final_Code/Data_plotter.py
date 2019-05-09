import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

leftWhisk = []
rightWhisk = []
with open('FlatTerrainData.csv', mode='r') as TrainingData:
    TrainingDataReader = csv.reader(TrainingData, delimiter=',')
    for row in TrainingDataReader:
        row[0] = int(row[0])
        row[1] = int(row[1])
        leftWhisk.append(row[0])
        rightWhisk.append(row[1])

plt.figure(1)
plt.subplot(2,1,1)
#plt.ylim(0, 1023)
plt.plot(leftWhisk)
plt.xlabel('Left Whisker')
plt.ylabel('Resolution')

plt.figure(1)
plt.subplot(2,1,2)
#plt.ylim(0, 1023)
plt.plot(rightWhisk)
plt.xlabel('Right Whisker')
plt.ylabel('Resolution')

plt.show()