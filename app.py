import base64
from datetime import datetime
import random
import string
from io import BytesIO

import flask

from flask import request
from matplotlib.figure import Figure

app = flask.Flask(__name__)


@app.route('/isAlive')
def is_alive():
    return 'sensor-data-reader is alive!'


@app.route('/')
def bind_index():
    return flask.render_template('index.html')


@app.route('/csv_data/text', methods=['POST'])
def parse_csv_text():
    text_data = request.data.decode()
    return on_csv_data(text_data)


@app.route('/csv_data/file', methods=['POST'])
def parse_csv_file():
    csv_file = request.files["file"]
    text_data = csv_file.read().decode("utf-8")
    return on_csv_data(text_data)


def on_csv_data(csv_content):
    data = CsvParser().parse_csv_text(csv_content)

    x_date = list(map(lambda e: e['date'], data))
    y_temp1 = list(map(lambda e: e['temp_1'], data))
    y_temp2 = list(map(lambda e: e['temp_2'], data))
    y_temp3 = list(map(lambda e: e['temp_3'], data))

    figure = ChartGenerator().temp_chart_fig(x_date, y_temp1, y_temp2, y_temp3)
    buf = BytesIO()
    figure.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


class CsvParser:
    def parse_csv_text(self, text):
        text = text.replace("\ufeff", "")
        rows = text.split("\r\n")
        data = []
        for i in range(1, len(rows) - 1):
            row = rows[i]
            cols = row.split(",")
            data.append({
                'temp_1': float(cols[0]),
                'temp_2': float(cols[1]),
                'temp_3': float(cols[2]),
                'humidity_1': float(cols[3]),
                'humidity_2': float(cols[4]),
                'humidity_3': float(cols[5]),
                'speed': float(cols[6]),
                'presence_1': bool(int(cols[7])),
                'presence_2': bool(int(cols[8])),
                'date': datetime.strptime(cols[9], '%H:%M:%S %p'),
                'index': int(cols[11]),
            })
        return data


class ChartGenerator:
    def temp_chart_fig(self, x, temp_1, temp_2, temp_3):
        fig = Figure()
        ax = fig.subplots()
        ax.plot(x, temp_1, alpha=0.3, color='red', marker='o', label="temperature 1")
        ax.plot(x, temp_2, alpha=0.3, color='blue', marker='o', label="temperature 2")
        ax.plot(x, temp_3, alpha=0.3, color='green', marker='o', label="temperature 3")
        ax.grid(True)
        ax.legend()
        return fig;

    def random_name(self, nr_of_chars):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(nr_of_chars))


if __name__ == '__main__':
    app.run()
