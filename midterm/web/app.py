import json
import random
from flask import Flask, request
import redis
import datetime
rd=redis.StrictRedis(host='ig7235-redis',port=6379, db=0)


app = Flask(__name__)
#main flas app, root of flask app


@app.route('/hello/<name>', methods=['GET'])
def hello_name(name):
    return 'Hello {} \n'.format(name)    

@app.route('/hello', methods=['GET'])
def hello_name1():
    name = request.args.get('name')
    return '(round2) Hello {}\n'.format(name)

# using json file to access data 

@app.route('/animals', methods=['GET'])
def get_animals():
    return json.dumps(get_data())

@app.route('/animals/head/<animal>', methods=['GET'])
def get_animals_head_bunny(animal):
   all_animals_dict = get_data()
   head_animal_dict ={} 
   
   for i,j in all_animals_dict.items():
      if (all_animals_dict[i]['head'] == animal):
         head_animal_dict[i] = j

   return json.dumps(head_animal_dict)      
         
@app.route('/animals/legs/<num>', methods=['GET'])
def get_animals_legs_num(num):
   num = int(num)
   all_animals_dict = get_data()
   num_legs_dict = {}
   
   for i,j in all_animals_dict.items():
      if(all_animals_dict[i]['legs'] == num):
         num_legs_dict[i] = j    
   
   return json.dumps(num_legs_dict)


def get_data():
    with open('data_file.json', 'r') as f:
        animals = json.load(f)
    return animals


# using redis to access data and edit
@app.route('/animals/<date_1>/<date_2>', methods=['GET'])
def get_range_date_query(date_1,date_2):
   date_1obj = datetime.date.strptime(date_1,'%Y-%m-%d')
   date_2obj = datetime.date.strptime(date_2,'%Y-%m-%d')
   list_animals_uuid = rd.keys()
   list_animals_date_range = []
   for i in list_animals_uuid:
      date = rd.hget(i,'created_on').decode('utf-8')
      dateobj = datetime.date.strptime(date, '%Y-%m-%d')
      if(dateobj > date_1obj and dateobj < date_2obj):
         list_animals_date_range.append(i.convert('utf-8'))
   #returns list of uuid of animals who where created on said range
   return tuple(list_animals_date_range)
   


@app.route('/animals/<uuid>', methods=['GET'])
def get_animals_by_uuid(uuid):
   uuid = str(uuid)
   animal = rd.hgetall(uuid)
   # change from binary str to normal str
   animal_decoded = {}
   for key, value in animal.items():
      animal_decoded[key.decode('utf-8')] = value.decode('utf-8')
   
   return(animal_decoded)

@app.route('/animals/edit/<uuid>/<part>/<new_part>', methods=['GET'])
def edit_animal_by_uuid(uuid, part, new_part):
   uuid = str(uuid)
   old_animal = rd.hgetall(uuid)
   new_animal_decoded = {}
   for key, value in  old_animal.items():
      new_animal_decoded[key.decode('utf-8')] = value.decode('utf-8')
   new_animal_decoded[part] = new_part

   rd.hmset(uuid,new_animal_decoded)
   return new_animal_decoded

@app.route('/animals/delete/<date_1>/<date_2>', methods=['GET'])
def delete_animals_range_date(date_1,date_2):
   date_1obj = datetime.date.strptime(date_1,'%Y-%m-%d')
   date_2obj = datetime.date.strptime(date_2,'%Y-%m-%d')
   list_animals_uuid = rd.keys()
   list_animals_date_range = []
   for i in list_animals_uuid:
      date = rd.hget(i,'created_on').decode('utf-8')
      dateobj = datetime.date.strptime(date, '%Y-%m-%d')
      if(dateobj > date_1obj and dateobj < date_2obj):
         rd.hdel(i)
   #returns list of uuid of animals who where created on said range
   return tuple(list_animals_date_range)





@app.route('/animals/avarage/legs', methods=['GET'])
def get_animals_avarage_legs():
   list_animals_uuid = rd.keys()
   total_animals = len(list_animals_uuid)
 
   sum_legs = 0
   for i in list_animals_uuid:
       num_legs =int( rd.hget(i, 'legs'))
       sum_legs += num_legs

   avarage = sum_legs/total_animals
   return(str(avarage))

@app.route('/animals/count', methods=['GET'])
def get_animals_count():
   list_animals_uuid = rd.keys()
   animals_count = len(list_animals_uuid)
   return(str(animals_count))


if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0')
