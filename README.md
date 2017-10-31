# Insight Data Engineering Coding Challenge

Coding challenge solution for the Insight Data Engineering Fellowship.

## Getting Started

The following sections provide information about approach, prerequisites and run instructions.

### Approach

For this project, I have created a single data processing file, ```./src/find_political_donors.py``` 
that does all the lifting. Input and output file locations are passed in the command line arguments. See 
Running Instructions for detailed steps. When the project is initiated,
1. The program starts processing political donations data from the input file.
2. As each donor's information arrives, the program parses the data and validates it under input constraints.
3. Algorithm overview:
	* The information is processed by maintaining two Hash Maps, one for processing data by zip codes and another by transaction dates.
	* Each pair of ```(CMTE_ID, ZIP_CODE)``` and ```(CMTE_ID, TXN_DATE)``` maintains a min heap and max heap for calculation of running medians.
	* Processed output is written in the output files.
4. Batch processing can improve processing, but as mentioned in the challenge, the program should be capable of handling online data. Hence, I went with
processing data by one line at a time.

### Prerequisites

The project is developed in Python, version 2.7.12.
###### Default libraries used
- os, sys, getopt, datetime
- heapq

### Running Instructions

##### Help
```
bash ./help.sh
```

##### Run program
```
bash ./run.sh
```

##### Run tests
```
cd insight_testsuite
bash ./run_tests.sh
```
Currently there are 3 test cases present. Although the code was tested against 1GB of data but could not upload due to upload size limitations.

### Test Cases explained

A brief overview of the test cases present:
- test_1 - validates the directory structure and default test case (provided).
- test_2 - validates the input constraints and running median calculation.
- test_3 - edge case where no valid data
