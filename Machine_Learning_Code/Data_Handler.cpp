#include "Data_Handler.h"
using namespace std;

Data_Handler::Data_Handler() : fileName("DataFile") {}

Data_Handler::Data_Handler(string thisFile) : fileName(thisFile) {}

vector<float> Data_Handler::getData() {
    ifstream myDataFile(fileName);

    if (myDataFile.is_open) {
        while(getline(myDataFile, ))
    }
}
