import flask

app = flask.Flask(__name__)


@app.route('/isAlive')
def is_alive():
    return 'sensor-data-reader is alive!'


@app.route('/')
def index():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run()
