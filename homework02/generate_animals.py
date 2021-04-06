#!/usr/bin/env python3
import json
import petname
import random
import sys
head_generator = ['bull', 'lion', 'raven', 'bunny']
arm_generator = [2,4,6,8,10]
leg_generator = [3,6,9,12]
animals = {}

for i in range (20):
	animals[i] = {}
	animals[i]['head'] = random.choice(head_generator)  
	
	body1 = petname.name()
	body2 = petname.name()
	animals[i]['body'] = ('{}-{}').format(body1, body2)
	
	animals[i]['arms'] = random.choice(arm_generator)
	animals[i]['legs'] = random.choice(leg_generator)
	animals[i]['tail'] = animals[i]['arms']+animals[i]['legs']

with open('/data/animals.json', 'w') as out:
	json.dump(animals, out, indent=2)

	



