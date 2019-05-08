# Tensorflow tutorial was used. https://www.tensorflow.org/tutorials/keras/basic_classification#explore_the_data
import tensorflow as tf
from tensorflow import keras
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def dataHandler(labelNumber, csvFileName, train_data, train_labels):
    # Creates lists
    leftWhisk = []
    rightWhisk = []
    with open(csvFileName, mode='r') as TrainingData:
        TrainingDataReader = csv.reader(TrainingData, delimiter=',')
        for row in TrainingDataReader:
            row[0] = int(row[0])
            row[1] = int(row[1])
            leftWhisk.append(row[0])
            rightWhisk.append(row[1])

    leftWhisk = np.asarray(leftWhisk) # Converts list to array
    rightWhisk = np.asarray(rightWhisk)
    leftWhisk = leftWhisk/1023 # Scales data down to 0-1
    rightWhisk = rightWhisk/1023

    myTrainData = np.array([])
    myTrainLabels = np.array([])
    class_names = ['Flat Terrain', 'Rough Terrain', 'Wall', 'Small Object']

    appendFlag = 1
    i = 0
    j = 0

    while appendFlag == 1:
        whiskSection = leftWhisk[i:i+100]
        #if i == 0:
        #    myTrainData = np.array([whiskSection])
        #    myTrainLabels = np.array(0)
        #else:
        myTrainData = np.append(myTrainData,[whiskSection])
        myTrainLabels = np.append(myTrainLabels,labelNumber)
        #print(train_data)
        i+=100
        j+=1
        if ((len(leftWhisk) - i) < 100):
            appendFlag = 0

    appendFlag = 1
    i = 0

    while appendFlag == 1:
        whiskSection = rightWhisk[i:i+100]
        myTrainData = np.append(myTrainData,[whiskSection])
        myTrainLabels = np.append(myTrainLabels,labelNumber)
        #print(train_data)
        i+=100
        j+=1
        if ((len(rightWhisk) - i) < 100):
            appendFlag = 0

    myTrainData = np.reshape(myTrainData,(j,100))
    #myTrainLabels = np.reshape(myTrainLabels,(j,1))
    myTrainLabels = myTrainLabels.astype(int)

    print(myTrainData)
    print(myTrainLabels)

    plt.figure(figsize=(10,10))
    for k in range(6):
        plt.subplot(3,2,k+1)
        #plt.xticks([])
        #plt.yticks([])
        #plt.grid(False)
        #plt.imshow(train_data[k], cmap=plt.cm.binary)
        plt.plot(myTrainData[k])
        plt.xlabel(class_names[myTrainLabels[k]])
    plt.show()

    #print("end")
    train_data = np.append(train_data, myTrainData)
    train_labels = np.append(train_labels, myTrainLabels)
    return train_data, train_labels


def trainingAlgorithm(train_data, train_labels):
    model = keras.Sequential([
    #keras.layers.Flatten(input_shape=(100,)),
    keras.layers.Dense(20, activation=tf.nn.relu),
    #keras.layers.Dense(10, activation=tf.nn.relu),
    #keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    model.compile(optimizer='adam',
    loss='sparse_categorical_crossentropy', 
    metrics=['accuracy'])

    model.fit(train_data, train_labels, epochs=5)


def main():
    train_data = np.array([])
    train_labels = np.array([])

    #labelNumber = 0
    #csvFileName = 'TrainingData.csv'
    #train_data, train_labels = dataHandler(labelNumber, csvFileName, train_data, train_labels)

    labelNumber = 0
    csvFileName = 'FlatTerrainData.csv'
    train_data, train_labels = dataHandler(labelNumber, csvFileName, train_data, train_labels)

    labelNumber = 1
    csvFileName = 'RoughTerrainData.csv'
    train_data, train_labels = dataHandler(labelNumber, csvFileName, train_data, train_labels)

    labelNumber = 2
    csvFileName = 'WallData.csv'
    train_data, train_labels = dataHandler(labelNumber, csvFileName, train_data, train_labels)

    labelNumber = 3
    csvFileName = 'SmallObjectData.csv'
    train_data, train_labels = dataHandler(labelNumber, csvFileName, train_data, train_labels)

    numSections = int(len(train_data)/100)
    train_data = np.reshape(train_data,(numSections,100))

    trainingAlgorithm(train_data, train_labels)

    #while True:
    #    pass



if __name__== "__main__":
    main()

