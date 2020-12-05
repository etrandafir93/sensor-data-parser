import flask
from flask import request

app = flask.Flask(__name__)


@app.route('/isAlive')
def is_alive():
    return 'sensor-data-reader is alive!'


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/upload_csv', methods=['POST'])
def upload_file():

        print(123)
        # csvfile = request.files['sensor_data.csv']
        file = request.files['file']
        if file:
            print('**found file', file.filename)


        # reader = csv.DictReader(csvfile)
        # data = [row for row in reader]

if __name__ == '__main__':
    app.run()
