import base64
from datetime import datetime
import random
import string
from io import BytesIO
import flask

from flask import request, Response
from matplotlib.figure import Figure

app = flask.Flask(__name__)


@app.before_first_request
def load_global_data():
    global chart_generator
    chart_generator = ChartGenerator()


@app.route('/isAlive')
def is_alive():
    return 'sensor-data-reader is alive!'


@app.route('/')
def bind_index():
    return flask.render_template('index.html')


@app.route('/csv_data/text', methods=['POST'])
def parse_csv_text():
    text_data = request.data.decode()
    key = on_csv_data(text_data)
    return generate_links_response(key)


@app.route('/csv_data/file', methods=['POST'])
def parse_csv_file():
    csv_file = request.files["file"]
    text_data = csv_file.read().decode("utf-8")
    key = on_csv_data(text_data)
    return generate_links_response(key)


@app.route('/chart/<chart_key>/<chart_type>/base64', methods=['GET'])
def get_chart_base64(chart_key, chart_type):
    resp = chart_generator.get_base64_chart(chart_key + "-" + chart_type)
    return Response(resp, mimetype='text/plain')


@app.route('/chart/<chart_key>/<chart_type>/html', methods=['GET'])
def get_chart_html(chart_key, chart_type):
    resp = '<img src="data:image/png;base64, {0}" alt="error" />'.format(
        chart_generator.get_base64_chart(chart_key + "-" + chart_type))
    return Response(resp, mimetype='text/html')


def generate_links_response(chart_key):
    return {
        'key': chart_key,
        'charts': {
            'html': {
                'temperature': '/chart/{0}/temperature/html'.format(chart_key),
                'humidity': '/chart/{0}/humidity/html'.format(chart_key),
                'speed': '/chart/{0}/speed/html'.format(chart_key),
                'presence1': '/chart/{0}/presence1/html'.format(chart_key),
                'presence2': '/chart/{0}/presence2/html'.format(chart_key),
            },
            'base64': {
                'temperature': '/chart/{0}/temperature/base64'.format(chart_key),
                'humidity': '/chart/{0}/humidity/base64'.format(chart_key),
                'speed': '/chart/{0}/speed/base64'.format(chart_key),
                'presence1': '/chart/{0}/presence1/base64'.format(chart_key),
                'presence2': '/chart/{0}/presence2/base64'.format(chart_key),
            }
        }
    }


def on_csv_data(csv_content):
    sensor_data = SensorData(csv_content)
    base_name = random_name(10)
    measurement_dates = sensor_data.get_dates()

    chart_generator.temp_chart(measurement_dates, sensor_data.get_temperature_data(), base_name)
    chart_generator.humidity_chart(measurement_dates, sensor_data.get_humidity_data(), base_name)
    chart_generator.speed_chart(measurement_dates, sensor_data.get_speed_data(), base_name)
    chart_generator.presence_chart(sensor_data.get_presence_data("presence_1"), base_name, "1")
    chart_generator.presence_chart(sensor_data.get_presence_data("presence_2"), base_name, "2")

    return base_name


def random_name(nr_of_chars):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(nr_of_chars))


class ChartGenerator:

    def __init__(self):
        self.base64_charts_map = {}

    def get_base64_chart(self, chart_key):
        return self.base64_charts_map.get(chart_key)

    def presence_chart(self, data, base_name, sufix):
        labels = 'present', 'not present'
        fig = Figure()
        ax = fig.subplots()
        ax.pie(data, explode=(0, 0.1), labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal')
        chart_name = base_name + "-presence" + sufix
        self.save_as_base64(fig, chart_name)
        return chart_name;

    def speed_chart(self, x, y, base_name):
        fig = Figure()
        ax = fig.subplots()
        ax.plot(x, y, alpha=0.3, color='red', marker='o', label="speed")
        ax.grid(True)
        ax.legend()
        chart_name = base_name + "-speed"
        self.save_as_base64(fig, chart_name)
        return chart_name;

    def humidity_chart(self, x, humidity, base_name):
        (humidity_1, humidity_2, humidity_3) = humidity
        fig = Figure()
        ax = fig.subplots()
        ax.plot(x, humidity_1, alpha=0.3, color='red', marker='o', label="humidity 1")
        ax.plot(x, humidity_2, alpha=0.3, color='blue', marker='o', label="humidity 2")
        ax.plot(x, humidity_3, alpha=0.3, color='green', marker='o', label="humidity 3")
        ax.grid(True)
        ax.legend()

        chart_name = base_name + "-humidity"
        self.save_as_base64(fig, chart_name)
        return chart_name;

    def temp_chart(self, x, temperatures, base_name):
        (temp_1, temp_2, temp_3) = temperatures
        fig = Figure()
        ax = fig.subplots()
        ax.plot(x, temp_1, alpha=0.3, color='red', marker='o', label="temperature 1")
        ax.plot(x, temp_2, alpha=0.3, color='blue', marker='o', label="temperature 2")
        ax.plot(x, temp_3, alpha=0.3, color='green', marker='o', label="temperature 3")
        ax.grid(True)
        ax.legend()

        chart_name = base_name + "-temperature"
        self.save_as_base64(fig, chart_name)
        return chart_name;

    def save_as_base64(self, fig, key):
        buf = BytesIO()
        fig.savefig(buf, format="png")
        base64_img = base64.b64encode(buf.getbuffer()).decode("ascii")
        self.base64_charts_map[key] = base64_img


class SensorData:

    def __init__(self, csv_text_content):
        self.data = self.parse_csv_text(csv_text_content)
        print(self.data)

    def parse_csv_text(self, text):
        text = text.replace("\ufeff", "")
        rows = text.split("\n")
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

    def get_dates(self, ):
        return list(map(lambda e: e['date'], self.data))

    def get_presence_data(self, presence_key):
        positives = len(list(filter(lambda e: e[presence_key], self.data)))
        negatives = len(self.data) - positives
        return positives, negatives

    def get_speed_data(self):
        return list(map(lambda e: e['speed'], self.data))

    def get_humidity_data(self):
        y1 = list(map(lambda e: e['humidity_1'], self.data))
        y2 = list(map(lambda e: e['humidity_2'], self.data))
        y3 = list(map(lambda e: e['humidity_3'], self.data))
        return y1, y2, y3

    def get_temperature_data(self):
        y1 = list(map(lambda e: e['temp_1'], self.data))
        y2 = list(map(lambda e: e['temp_2'], self.data))
        y3 = list(map(lambda e: e['temp_3'], self.data))
        return y1, y2, y3


if __name__ == '__main__':
    app.run(port=5000)
