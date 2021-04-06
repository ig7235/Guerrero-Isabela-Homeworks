#!/usr/bin/env python3
import json
import random
import sys
#open json file 
def getedata():
   with open(sys.argv[1], 'r') as f:
      animals = json.load(f)
      random_animal = int(random.uniform(0,19))
      type(animals[str(random_animal)])
     # print(animals[str(random_animal)])
   return animals

test = getdata()
# print(test)
output = [x for x in test if x['head'] == 'snake' ]
print(output)


