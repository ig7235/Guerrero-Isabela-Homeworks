import json
import random

#open json file 

with open('animals.json', 'r') as f:
	animals = json.load(f)

random_animal = int(random.uniform(0,19))

type(animals[str(random_animal)])
print(animals[str(random_animal)])
