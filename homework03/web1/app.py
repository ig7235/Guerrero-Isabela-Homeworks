import json
import random
from flask import Flask, request

app = Flask(__name__)
#main flas app, root of flask app


@app.route('/hello/<name>', methods=['GET'])
def hello_name(name):
    return 'Hello {} \n'.format(name)    

@app.route('/hello', methods=['GET'])
def hello_name1():
    name = request.args.get('name')
    return '(round2) Hello {}\n'.format(name)



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
    with open('animals.json', 'r') as f:
        animals = json.load(f)
    return animals

if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0')
