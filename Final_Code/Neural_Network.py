# Tensorflow tutorial was used. https://www.tensorflow.org/tutorials/keras/basic_classification#explore_the_data
# https://keras.io/
import tensorflow as tf
from tensorflow import keras
import csv
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
import random

# Data handler function takes all data from csv files and converts it to data to be inputted
# into the neural network.
def dataHandler(labelNumber, csvFileName, train_data, train_labels, test_data, test_labels):
    # Creates lists
    leftWhisk = []
    rightWhisk = []
    # Opens desired csv file in read mode, and calls it TrainingData.
    # Iterates through each row of csv file and converts both values on
    # that row to ints. The first value is appended to the left whisker
    # data list and the second value is appended to the right whisker data
    # list.
    with open(csvFileName, mode='r') as TrainingData:
        TrainingDataReader = csv.reader(TrainingData, delimiter=',')
        for row in TrainingDataReader:
            row[0] = int(row[0])
            row[1] = int(row[1])
            leftWhisk.append(row[0])
            rightWhisk.append(row[1])

    leftWhisk = np.asarray(leftWhisk) # Converts list to array
    rightWhisk = np.asarray(rightWhisk) # Converts list to array
    leftWhisk = leftWhisk/1023 # Scales data from 0-1023 down to 0-1
    rightWhisk = rightWhisk/1023 # Scales data from 0-1023 down to 0-1

    # Create two empty arrays which will hold formatted whisker data and labels
    myTrainData = np.array([])
    myTrainLabels = np.array([])
    # Labels are identifed as a list (0->3) for labelling the graphs below
    class_names = ['Flat Terrain', 'Rough Terrain', 'Wall', 'Object Twang']

    # Create two empty arrays to hold the test data and labels
    myTestData = np.array([])
    myTestLabels = np.array([])

    testPercent = 5         # % of entire data which is test data
    trainDataCounter = 0    # Used to count number of 50 sample sections are being added to 'myTrainData'
    appendFlag = 1          # Flag which 
    i = 0                   # 
    j = 0                   # Counts number of 50 section samples added to 'myTrainData' for reshaping later
    m = 0                   # Counts number of 50 section samples added to 'myTestData' for reshaping later

    # Loop to take all data from left whisker and append it to 
    while appendFlag == 1:
        whiskSection = leftWhisk[i:i+50]    # 
        #whiskSection = (whiskSection - whiskSection.min())/(whiskSection.max() - whiskSection.min()) # Normalises data section
        # When counter increases to equal 100/testPercent (10%, 1 in 10), appends data to 'myTestData'
        if (trainDataCounter >= (100/testPercent)):
            myTestData = np.append(myTestData,[whiskSection])   # Appends the selected 50 data samples to 'myTestData'
            myTestLabels = np.append(myTestLabels,labelNumber)  # Appends the label for the current target data to 'myTestLabels'
            trainDataCounter = 0 # increases 'trainDataCounter'
            m+=1    # increases m counter

        # Otherwise data is appended to 'myTrainData'
        else:
            myTrainData = np.append(myTrainData,[whiskSection])     # Appends the selected 50 data samples to 'myTrainData'
            myTrainLabels = np.append(myTrainLabels,labelNumber)    # Appends the label for the current target data to 'myTrainLabels'
            j+=1    # increases j counter 
        #print(train_data) # Here for debugging purposes
        i+=50   # increases i counter
        trainDataCounter+=1 # increases 'trainDataCounter'
        if ((len(leftWhisk) - i) < 50):
            appendFlag = 0

    appendFlag = 1
    i = 0
    trainDataCounter = 0

    # Loop to take all data from right whisker and append it to 
    while appendFlag == 1:
        whiskSection = rightWhisk[i:i+50]
        #whiskSection = (whiskSection - whiskSection.min())/(whiskSection.max() - whiskSection.min()) # Normalises data section
        if (trainDataCounter >= (100/testPercent)):
            myTestData = np.append(myTestData,[whiskSection])
            myTestLabels = np.append(myTestLabels,labelNumber)
            trainDataCounter = 0
            m+=1
        else:
            myTrainData = np.append(myTrainData,[whiskSection])
            myTrainLabels = np.append(myTrainLabels,labelNumber)
            j+=1
        #print(train_data)  # Here for debugging purposes
        i+=50
        trainDataCounter+=1
        if ((len(rightWhisk) - i) < 50):
            appendFlag = 0

    myTrainData = np.reshape(myTrainData,(j,50))    # Reshapes training data to arrays of 50 samples long
    #myTrainLabels = np.reshape(myTrainLabels,(j,1))
    myTrainLabels = myTrainLabels.astype(int)       # Makes sure all the training data labels are ints

    myTestData = np.reshape(myTestData,(m,50))      # Reshapes testing data to arrays of 50 samples long
    myTestLabels = myTestLabels.astype(int)         # Makes sure all the testing data labels are ints
    '''
    print(myTrainData)
    print(myTrainLabels)
    print(myTestData)
    print(myTestLabels)
    print(len(myTrainData))
    print(len(myTestData))
    '''
    '''
    # Plots figures for each target for observation of recorded data
    plt.figure(num=labelNumber+1, figsize=(10,10))
    for k in range(16):
        plt.subplot(4,4,k+1)
        plt.ylim (-1,1)
        #thisPlot.set_autoscaley_on(False)
        plt.plot(myTrainData[k+random.randint(0,200)]) # Takes random section of data to be plotted
        #plt.plot(myTrainData[k])
        plt.xlabel(class_names[myTrainLabels[k]])
      '''

    # Following lines append training/testing data/labels from the current 
    # csv file to the arrays to be returned to the main function
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
    # Creates a Keras Sequential model, which is an ordinary Artificial Neural
    # Network with Dense layers (regular connected layer). 'model.add' adds a new
    # layer to the network, where the number of nodes in the layer is first defined
    # followed by the activation function, and if it is the first layer of 
    # the network, the input dimmensions defined.
    model = keras.Sequential()
    model.add(keras.layers.Dense(24, activation=tf.nn.relu, input_dim=50))
    #model.add(keras.layers.GaussianNoise(0.3))
    #model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dropout(0.3))
    #model.add(keras.layers.Dense(8, activation=tf.nn.relu))
    #model.add(keras.layers.BatchNormalization())
    #model.add(keras.layers.Dropout(0.5))
    #model.add(keras.layers.Dense(17, activation=tf.nn.relu))
    model.add(keras.layers.Dense(4, activation=tf.nn.softmax))

    # Optimizer's parameters are altered here. 
    opt = keras.optimizers.Nadam()
    model.compile(
        optimizer=opt,  # Optimizer set here
        loss='sparse_categorical_crossentropy', # Loss function for this NN. The number the NN is trying to decrease
        metrics=['accuracy']    # Accuracy of neural network shown during training 
    )
    # Training of the model with training data and labels. Number of epochs are set, data is shuffled
    # after each epoch and validation data is set
    myHistory = model.fit(train_data, train_labels, epochs=200, shuffle=True, validation_split=0.05)

    model.evaluate(test_data, test_labels, batch_size=32) # Evaluates model with test data

    model.save('MLRobot.h5') # Saves the model in the file MLRobot.h5 which can be read by Tensorflow Keras

    # Plots validation and training accuracy
    plt.figure(0)
    plt.plot(myHistory.history['acc'])
    plt.plot(myHistory.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    #plt.show()
    # Plots validation and training loss
    plt.figure(1)
    plt.plot(myHistory.history['loss'])
    plt.plot(myHistory.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    #plt.show()
    '''
    input_arr = test_data[0]
    #myData = myData.T
    input_arr = np.expand_dims(input_arr, axis=0)
    predictions = model.predict(input_arr) 
    print(predictions)
    print(input_arr.shape)
    print(np.argmax(model.predict(input_arr)))
    
    weights = model.layers[0].get_weights()[0]
    biases = model.layers[0].get_weights()[1]
    np.save('Layer0Weights.npy', weights)
    np.save('Layer0Biases.npy', biases)
    #loaded = np.load('Layer0Weights.npy')
    weights = model.layers[1].get_weights()[0]
    biases = model.layers[1].get_weights()[1]
    np.save('Layer1Weights.npy', weights)
    np.save('Layer1Biases.npy', biases)
    weights = model.layers[2].get_weights()[0]
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
    # Creating empty arrays to hols all the data
    train_data = np.array([])
    train_labels = np.array([])
    test_data = np.array([])
    test_labels = np.array([])

    # label number is the target of this file of data. So all the data contained in the 'FlatTerrain.csv' is from when the 
    # robot was on flat terrain. Flat terrrain data is target number 0. Same appraoch for all collected data below.
    # 'dataHandler()' formats the csv data, appends that to the combined data arrays which are returned.
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

    # Data arrays need to be reshaped to fit the NN model. The datasets are multidimensional arrays, with the arrays within the
    # main array, length 50 samples.
    numSections = int(len(train_data)/50)
    train_data = np.reshape(train_data,(numSections,50))

    numSections = int(len(test_data)/50)
    test_data = np.reshape(test_data,(numSections, 50))

    # 'trainingAlgorithm' function called which is where NN will be trained
    trainingAlgorithm(train_data, train_labels, test_data, test_labels)

    # Used to display plots created in the code
    plt.show()

if __name__== "__main__":
    main()

