# Tensorflow tutorial was used. https://www.tensorflow.org/tutorials/keras/basic_classification#explore_the_data
# https://keras.io/
import tensorflow as tf
from tensorflow import keras
import csv
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
import random

def dataHandler(labelNumber, csvFileName, train_data, train_labels, test_data, test_labels):
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
    class_names = ['Flat Terrain', 'Rough Terrain', 'Wall', 'Object Twang']

    myTestData = np.array([])
    myTestLabels = np.array([])
    testPercent = 10 # %

    appendFlag = 1
    i = 0
    j = 0
    testDataCounter = 0
    m = 0
    while appendFlag == 1:
        whiskSection = leftWhisk[i:i+50]
        whiskSection = (whiskSection - whiskSection.min())/(whiskSection.max() - whiskSection.min())
        if (testDataCounter >= (100/testPercent)):
            myTestData = np.append(myTestData,[whiskSection])
            myTestLabels = np.append(myTestLabels,labelNumber)
            testDataCounter = 0
            m+=1
        #if i == 0:
        #    myTrainData = np.array([whiskSection])
        #    myTrainLabels = np.array(0)
        else:
            myTrainData = np.append(myTrainData,[whiskSection])
            myTrainLabels = np.append(myTrainLabels,labelNumber)
            j+=1
        #print(train_data)
        i+=50
        testDataCounter+=1
        if ((len(leftWhisk) - i) < 50):
            appendFlag = 0

    appendFlag = 1
    i = 0
    testDataCounter = 0

    while appendFlag == 1:
        whiskSection = rightWhisk[i:i+50]
        whiskSection = (whiskSection - whiskSection.min())/(whiskSection.max() - whiskSection.min())
        if (testDataCounter >= (100/testPercent)):
            myTestData = np.append(myTestData,[whiskSection])
            myTestLabels = np.append(myTestLabels,labelNumber)
            testDataCounter = 0
            m+=1
        else:
            myTrainData = np.append(myTrainData,[whiskSection])
            myTrainLabels = np.append(myTrainLabels,labelNumber)
            j+=1
        #print(train_data)
        i+=50
        testDataCounter+=1
        if ((len(rightWhisk) - i) < 50):
            appendFlag = 0

    myTrainData = np.reshape(myTrainData,(j,50))
    #myTrainLabels = np.reshape(myTrainLabels,(j,1))
    myTrainLabels = myTrainLabels.astype(int)

    myTestData = np.reshape(myTestData,(m,50))
    myTestLabels = myTestLabels.astype(int)
    '''
    print(myTrainData)
    print(myTrainLabels)
    print(myTestData)
    print(myTestLabels)
    print(len(myTrainData))
    print(len(myTestData))
    '''
    '''
    plt.figure(num=labelNumber+1, figsize=(10,10))
    for k in range(16):
        plt.subplot(4,4,k+1)
        plt.ylim (-1,1)
        #thisPlot.set_autoscaley_on(False)
        plt.plot(myTrainData[k+random.randint(0,200)])
        #plt.plot(myTrainData[k])
        plt.xlabel(class_names[myTrainLabels[k]])
      '''
    #plt.show()
    train_data = np.append(train_data, myTrainData)
    train_labels = np.append(train_labels, myTrainLabels)
    test_data = np.append(test_data, myTestData)
    test_labels = np.append(test_labels, myTestLabels)
    return train_data, train_labels, test_data, test_labels


def trainingAlgorithm(train_data, train_labels, test_data, test_labels):
    '''model = keras.Sequential([
    #keras.layers.Flatten(input_shape=(50,1)),
    keras.layers.Dense(20, activation=tf.nn.relu),
    #keras.layers.Dense(20, activation=tf.nn.relu),
    keras.layers.Dense(8, activation=tf.nn.relu),
    #keras.layers.Dense(10, activation=tf.nn.relu),
    keras.layers.Dense(4, activation=tf.nn.softmax)
    ])'''
    # Creates a Keras Sequential model, which is a linear 
    model = keras.Sequential()
    model.add(keras.layers.Dense(20, activation=tf.nn.relu, input_dim=50))
    #model.add(keras.layers.BatchNormalization())
    #model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(10, activation=tf.nn.relu))
    #model.add(keras.layers.Dense(17, activation=tf.nn.relu))
    model.add(keras.layers.Dense(4, activation=tf.nn.softmax))

    opt = keras.optimizers.Adam(lr=0.002)
    model.compile(
        optimizer=opt,
        loss='sparse_categorical_crossentropy', # loss is 
        metrics=['accuracy']
    )

    model.fit(train_data, train_labels, epochs=1, shuffle=True, validation_split=0.05)

    model.evaluate(test_data, test_labels, batch_size=32)

    weights = model.layers[0].get_weights()[0]
    biases = model.layers[0].get_weights()[1]
    np.save('Layer0Weights.npy', weights)
    np.save('Layer0Biases.npy', biases)
    #loaded = np.load('Layer0Weights.npy')
    weights = model.layers[1].get_weights()[0]
    biases = model.layers[1].get_weights()[1]
    np.save('Layer1Weights.npy', weights)
    np.save('Layer1Biases.npy', biases)
    '''weights = model.layers[2].get_weights()[0]
    biases = model.layers[2].get_weights()[1]
    np.save('Layer2Weights.npy', weights)
    np.save('Layer2Biases.npy', biases)'''

    #print("Weights", weights)
    #print("Loaded Weights", loaded)
    #print("Biases", biases)

    

    #print("Weights", weights)
    #print("Biases", biases)
    #predictions = model.predict(test_data)
    #x = random.randint(0,248)
    #print(np.argmax(predictions[x]))
    #print(test_labels[x])




def main():
    train_data = np.array([])
    train_labels = np.array([])
    test_data = np.array([])
    test_labels = np.array([])
    #labelNumber = 0
    #csvFileName = 'TrainingData.csv'
    #train_data, train_labels = dataHandler(labelNumber, csvFileName, train_data, train_labels)

    labelNumber = 0
    csvFileName = 'FlatTerrainData.csv'
    train_data, train_labels, test_data, test_labels = dataHandler(labelNumber, csvFileName, train_data, train_labels, test_data, test_labels)
    #plt.figure(5)
    #plt.plot(train_data)

    labelNumber = 1
    csvFileName = 'RoughTerrainData.csv'
    train_data, train_labels, test_data, test_labels = dataHandler(labelNumber, csvFileName, train_data, train_labels, test_data, test_labels)
    #plt.figure(6)
    #plt.plot(train_data)

    labelNumber = 2
    csvFileName = 'WallData.csv'
    train_data, train_labels, test_data, test_labels = dataHandler(labelNumber, csvFileName, train_data, train_labels, test_data, test_labels)
    #plt.figure(7)
    #plt.plot(train_data)

    labelNumber = 3
    csvFileName = 'ObjectTwangData.csv'
    train_data, train_labels, test_data, test_labels = dataHandler(labelNumber, csvFileName, train_data, train_labels, test_data, test_labels)
    #plt.figure(8)
    #plt.plot(train_data)

    numSections = int(len(train_data)/50)
    train_data = np.reshape(train_data,(numSections,50))

    numSections = int(len(test_data)/50)
    test_data = np.reshape(test_data,(numSections, 50))

    trainingAlgorithm(train_data, train_labels, test_data, test_labels)

    plt.show()

if __name__== "__main__":
    main()

