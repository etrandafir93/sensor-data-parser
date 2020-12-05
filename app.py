
from flask import Flask
app = Flask(__name__)

@app.route('/isAlive')
def hello_world():
    return 'sensor-data-reader is alive!'

if __name__ == '__main__':
    app.run()