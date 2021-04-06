from flask import Flask, request
app = Flask(__name__)

@app.route('/',methods=['GET'])
def helloworld():
   return 'Hello from docker'

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')
