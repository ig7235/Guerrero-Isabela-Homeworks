import json
from flask import Flask, request

app = Flask(__name__)
#main flas app, root of flask app
1

@app.route('/hello/<name>', methods=['GET'])
def hello_name(name):
    return 'Hello {} \n'.format(name)    

@app.route('/hello', methods=['GET'])
def hello_name1():
    name = request.args.get('name')
    return '(round2) Hello {}\n'.format(name)



@app.route('/degrees', methods=['GET'])
def get_degrees():
    return json.dumps(get_data())

def get_data():
    return[{"hey":4,"how":4},{"hey": 4, "how":6}]


if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0')
