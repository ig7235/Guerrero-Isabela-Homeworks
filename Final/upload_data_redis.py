import json
import sys
import datetime
import uuid
import redis
import os

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd_dataset = redis.StrictRedis(host=redis_ip, port=6391, db=0, decode_responses=True)

with open('dataset.json', r) as data:
   years_data = json.load(data)

for i in years_data:
   key = str(i)
   value = years_data[i]
   rd_dataset.hmset(key,value)
