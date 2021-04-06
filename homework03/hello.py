import json
from flask import Flask

app = Flask(__name__)
#main flas app, root of flask app

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World! \n'

@app.route('/hello/<name>', methods=['GET'])
def hello_name(name):
    return 'Hello {} \n'.format(name)    

@app.route('/degrees', methods=['GET'])
def get_degrees():
    return json.dumps(get_data())

def get_data():
    return[{"hey":4,"how":4},{"hey": 4, "how":6}]


if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0')
