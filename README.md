# Final-Year-Project by Oisín Walsh

This repository includes all code used in the design and implementation of my project on a machine learning robot.
All code used in the final implementation of the robot is in located in the folder labelled 'Final_Code'. This folder includes the
following code files:

- 'Arduino_Code.ino' - Captures the sensor data and sends this data to the Raspberry Pi over UART, and controls the motors of the
robot after reading messages sent from the Pi.

- 'Rasp_Pi_Code.py' - Used during the capturing of the training data stage of the project. Reads in sensor data sent from Arduino and 
saves this data to an appropriately named csv file. Communicates over bluetooth with my phone using the app 'BlueTooth Serial Controller'
(Available here: https://play.google.com/store/apps/details?id=nextprototypes.BTSerialController). This app controls where the robot moves
(forwards, backwards, right, left, stop). This information is received by the Pi and sent to the Arduino.

- 'Neural_Network.py' - Reads in data used for training of neural network and trains a model using this data, with the Keras API on top
of TensorFlow. Model is saved as a '.h5' file type.

- 'Rasp_Pi_DeployedNN.py' - Deploys the trained neural network model onto the Raspberry Pi. Modified version of 'Rasp_Pi_Code.py', by 
removing the function to save the data and instead having code which loads in the model I chose, tests the collected samples with the model
and displays the resulting class to the OLED screen.

Also included in this folder are: 

- The trained neural network models, of file type '.h5'.

- The saved data files (in csv file format) was used for training of the neural network.

- An Adafruit library used to display text onto the OLED display on the robot.

Figures of some results obtained during the project are in the 'Results' folder.
