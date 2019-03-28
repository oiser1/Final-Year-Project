#ifndef NEURAL_NETWORK_H_INCLUDED
#define NEURAL_NETWORK_H_INCLUDED

#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <math.h>

using namespace std;

class Neural_Network {
private:
	vector<float> inputs;
	vector<float> targets;
	vector<float> trainingInputs;
	vector<float> validationInputs;
	vector<float> testInputs;
	int hiddenLayers;
	int nodesPerLayer[hiddenLayers] = {};

public:
	Neural_Network();
	vector<float> getTrainingData();
	vector<float> getValidationData();
	vector<float> getTestData();

	void setNumHiddenLayers(int);
	void setNumNodesPerLayer(int[f]);

}