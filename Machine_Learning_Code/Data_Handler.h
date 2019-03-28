//#ifndef DATA_HANDLER_H_INCLUDED
#define DATA_HANDLER_H_INCLUDED

#include <iostream>
#include <vector>
#include <fstream>
#include <string>

using namespace std;

class Data_Handler {
private:
    vector<float> inputs;
	vector<float> targets;
    string fileName;

public:
    Data_Handler();  // Default constructor
	Data_Handler(string);
    vector<float> getData();
}