import flask
from flask import request

app = flask.Flask(__name__)


@app.route('/isAlive')
def is_alive():
    return 'sensor-data-reader is alive!'


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/csv_data/text', methods=['POST'])
def parse_csv_text():
    text_data = request.data.decode()
    print(text_data)
    return "ok1"


@app.route('/csv_data/file', methods=['POST'])
def parse_csv_file():
    csv_file = request.files["file"]
    print(csv_file)
    return "ok2"



if __name__ == '__main__':
    app.run()
