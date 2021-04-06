import json
import petname
import random
import sys
import datetime
import uuid
import redis
rd=redis.StrictRedis(host='127.0.0.1',port=6391, db=0)

# generate animals 
head_generator = ['bull', 'lion', 'raven', 'bunny']
arm_generator = [2,4,6,8,10]
leg_generator = [3,6,9,12]
animals = {}

for i in range (20):
   uid = str(uuid.uuid4())
   animals[uid] = {}
   today = datetime.date.today()
   animals[uid]['created_on'] =str(today)
   animals[uid]['head'] = random.choice(head_generator)
   
   body1 = petname.name()
   body2 = petname.name()
   animals[uid]['body'] = ('{}-{}').format(body1, body2)

   animals[uid]['arms'] = random.choice(arm_generator)
   animals[uid]['legs'] = random.choice(leg_generator)
   animals[uid]['tail'] = animals[uid]['arms']+animals[uid]['legs']
   
# upload to redis database
for i in animals:
   key = str(i)
   value = animals[i]
   rd.hmset(key,value)

# upload to json file
with open('animals.json', 'w') as out:
        json.dump(animals, out, indent=2)


