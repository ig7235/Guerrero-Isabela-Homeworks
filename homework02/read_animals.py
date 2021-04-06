#!/usr/bin/env python3
import json
import random
import sys
#open json file 

def get_data():
    with open('/data/animals.json', 'r') as f:
        animals = json.load(f)
    return animals

# given key value of two animals in json file, return sum of number of legs
def num_legs_two_animals(x,y):
   all_animals = get_data()  

   if(x > len(all_animals) or y > len(all_animals) or x < 0 or y < 0):
      return ('animal does not exist')
   if(x == y):
      return ('x and y cannot be equal')

   x = str(x)
   y = str(y)
 
   total_legs = all_animals[x]['legs']+all_animals[y]['legs']
   return total_legs

def main():
   print(num_legs_two_animals(10,5))

if  __name__ == '__main__':
	main()


