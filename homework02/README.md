# README Homework 2

## Tools
1. python3:
   * Code in Docker runs on python version 3
2. petname:
   * There is the use of python library petname versiion 2.6 to execute somo of the animals' features
3. 'generate_animals.py' python script
   * Script randomly generates a dictinary of 20 visare animals, which are appened onto a json script animals.json
4. 'read_animals.py' python script
   * Script gets data from the json file with visare animals. I has two functions:
      - 'get_data()': opens json file, read, and returns animals.
      - 'num_legs_two_animals(x,y)': recieves index of two animals in the list and returns how many legs they have between the two.  
## Download script 

## Build image with Dockerfile provided


## Run script inside container

## Run unit tests
To run unit tests made for 'num_legs_two_animals(x,y)':
   1. Go to command line and type 'python3 read_animals_test.py'
   2. Unit test will verify that:
      * x and y input are of type int()
      * x and y fall between 0 and 19, other wise return such animals dont exist
      * x and y are not bool or strings 
      * right number of inputs are being used in when calling the function
   3. After running the script it should return:
      '''
      Ran 1 test in ....s
      OK 
      '''  
