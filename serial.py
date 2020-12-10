
import serial
from datetime import datetime as dt
sensor_out_csv_path = "../out/sensor_data_new.csv"

def main():

    ser = serial.Serial()
    ser.port = "COM5"
    ser.baudrate = 9600
    ser.open()
    while True:

        line = ser.readline().decode()
        data = line.split(";")
        speed = data[0].split(":")[1]

        humidity_1 = data[1].split(":")[1]
        humidity_2 = data[2].split(":")[1]
        humidity_3 = data[3].split(":")[1]
        temperature_1 = data[4].split(":")[1]
        temperature_2 = data[5].split(":")[1]
        temperature_3 = data[6].split(":")[1]
        presence_1 = data[7].split(":")[1]
        presence_2 = data[8].split(":")[1]
        date = dt.now().strftime("%Y-%m-%d %H:%M:%S")

        new_csv_row = "%s,%s,%s,%s,%s,%s,%s,%s,%s,,%s\n".format( temperature_1, temperature_2, temperature_3, humidity_1, humidity_2, humidity_3, speed, presence_1, presence_2, date )

        with open(sensor_out_csv_path, "a+") as f:
            f.write(new_csv_row)



if __name__ == '__main__':
    main()