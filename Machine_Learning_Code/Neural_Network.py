import tensorflow as tf
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Creates lists
leftWhisk = []
rightWhisk = []

def dataHandler(leftWhisk, rightWhisk):
    with open('TrainingData.csv', mode='r') as TrainingData:
            TrainingDataReader = csv.reader(TrainingData, delimiter=',')
            for row in TrainingDataReader:
                row[0] = int(row[0])
                row[1] = int(row[1])
                leftWhisk.append(row[0])
                rightWhisk.append(row[1])

            leftWhisk = np.asarray(leftWhisk) # Converts list to array
            rightWhisk = np.asarray(rightWhisk)
            leftWhisk = leftWhisk/1023
            rightWhisk = rightWhisk/1023

            class_names = ['Flat Terrain', 'Rough Terrain', 'Wall', 'Small Object', 'Nothing']

            appendFlag = 1
            i = 0
            j = 0

            while appendFlag == 1:
                whiskSection = leftWhisk[i:i+100]
                if i == 0:
                    train_data = np.array([whiskSection])
                    train_labels = np.array(0)
                else:
                    train_data = np.append(train_data,[whiskSection])
                    train_labels = np.append(train_labels,0)
                #print(train_data)
                i = i + 100
                j = j + 1
                if ((len(leftWhisk) - i) < 100):
                    appendFlag = 0

            appendFlag = 1
            i = 0

            while appendFlag == 1:
                whiskSection = rightWhisk[i:i+100]
                train_data = np.append(train_data,[whiskSection])
                train_labels = np.append(train_labels,0)
                #print(train_data)
                i = i + 100
                j = j + 1
                if ((len(rightWhisk) - i) < 100):
                    appendFlag = 0

            train_data = np.reshape(train_data,(j,100))
            #train_labels = np.reshape(train_labels,(j,1))

            print(train_data)
            print(train_labels)

            plt.figure(figsize=(10,10))
            for k in range(6):
                plt.subplot(3,2,k+1)
                plt.xticks([])
                plt.yticks([])
                plt.grid(False)
                #plt.imshow(train_data[k], cmap=plt.cm.binary)
                plt.plot(train_data[k])
                plt.xlabel(class_names[train_labels[k]])
            plt.show()

            #leftWhisk_Dataset = pd.DataFrame(leftWhisk)
            #rightWhisk_Dataset = pd.DataFrame(rightWhisk)
            #print(leftWhisk_Dataset[0:100])
            #print(leftWhisk_Dataset[100:200])
            #print(rightWhisk_Dataset)
            #print(leftWhisk)
            #plt.plot(leftWhisk)
            #plt.ylabel('Range')
            #plt.xlabel('Samples')
            #plt.show()
            #print("\n")
            #print(rightWhisk)
            #plt.plot(rightWhisk)
            #plt.ylabel('Range')
            #plt.xlabel('Samples')
            #plt.show()
            print("end")

#def trainingAlgorithm:


def main():
    dataHandler(leftWhisk, rightWhisk)
    while True:
        pass



if __name__== "__main__":
    main()

