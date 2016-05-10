__author__ = 'exiaohao@gmail.com'
import sys, os
import datetime
from influxdb import InfluxDBClient


class logger_tool(object):

    def __init__(self, name):
        self.name = name

    def disp_line(self, state, folder, classname, act, attr, fore, back):
        color = "\x1B[%d;%d;%dm" % (attr, fore, back)
        default_color = "\x1B[%d;%d;%dm" % (0, 0, 0)
        print("[{}] {}[{}]{}{}/{}:{} @ {}".format(self.name, color, state, default_color, folder, classname, act, datetime.datetime.now()))

    def disp_simple_line(self, state, act, attr, fore, back):
        color = "\x1B[%d;%d;%dm" % (attr, fore, back)
        default_color = "\x1B[%d;%d;%dm" % (0, 0, 0)
        line = "{}[{}]{} {} / {} / {}".format(color, state, default_color, self.name, act, datetime.datetime.now())
        print(line)

        path = os.path.abspath(__file__).rsplit("/", 2)[0]
        with open(path + '/log/request.txt', 'a+') as f:
            f.write(line)
            f.write('\n')
        # todo:insert2influxdb

    # Info
    def info(self, url, time):
        self.disp_simple_line("INFO", '{} time={}'.format(url, time), 0, 30, 42)

        json_body = [
            {
                "measurement": 'fetch_time',
                "tags": {
                    "host": "server01",
                    "region": "shanghai",
                    "target": url
                },
                "fields": {
                    "value": time
                }
            }
        ]
        client = InfluxDBClient(host='127.0.0.1', port=8086, username='tale', password='0541029b-4d66-4544', database='tale')
        # client.create_database('tale')
        client.write_points(json_body)
        # print('Insert InfluxDB:', result, json_body, '\n')
        # results = client.query('select value from fetch_time')
        # for result in results:
        #     print(result, '\n')

    # Fatal
    def fatal(self, act):
        self.disp_simple_line("FATAL", act, 0, 33, 41)
