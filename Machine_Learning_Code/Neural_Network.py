import tensorflow as tf
import csv
import matplotlib.pyplot as plt
import numpy as np

leftWhisk = []
rightWhisk = []

def dataHandler(leftWhisk, rightWhisk):
    #while (rowFlag == 
    with open('TrainingData.csv', mode='r') as TrainingData:
            TrainingDataReader = csv.reader(TrainingData, delimiter=',')
            for row in TrainingDataReader:
                row[0] = int(row[0])
                row[1] = int(row[1])
                leftWhisk.append(row[0])
                rightWhisk.append(row[1])

            leftWhisk = np.asarray(leftWhisk)
            rightWhisk = np.asarray(rightWhisk)
            #print(leftWhisk)
            plt.plot(leftWhisk)
            plt.ylabel('Range')
            plt.xlabel('Samples')
            plt.show()
            #print("\n")
            #print(rightWhisk)
            plt.plot(rightWhisk)
            plt.ylabel('Range')
            plt.xlabel('Samples')
            plt.show()
def main():
    dataHandler(leftWhisk, rightWhisk)
    while True:
        pass



if __name__== "__main__":
    main()

