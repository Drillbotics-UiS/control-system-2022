import json
import os
import random
import time
import unittest
from sqlite3 import connect

from data_models.dh_sensor_data import DHSensorData
from data_models.plc_sensor_data import PLCSensorData
from data_models.user_input import UserInput
from logger.logger import Logger


class TestLogger(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        configfile = open("config.json")
        config = json.load(configfile)
        configfile.close()
        self.lg = Logger(config["schema_file"],config["log_buffer_size"], 1)
        self.lg.run_logger = True
        self.conn = connect(self.lg.filename)

    def test_plc_log(self):
        k = random.randint(10, 1523)
        n = len(PLCSensorData.read_from_db(self.conn))
        for i in range(k):
            plc = PLCSensorData()
            plc.top_drive_rpm = i
            self.lg.log_PLC(plc)
        self.lg.flush_PLC_buffer()
        time.sleep(0.5)  # waiting for thread
        t = len(PLCSensorData.read_from_db(self.conn))
        self.assertEqual(k, t-n)

    def test_dh_log(self):
        k = random.randint(10, 1523)
        n = len(DHSensorData.read_from_db(self.conn))
        for i in range(k):
            dh = DHSensorData()
            dh.acc_x = i
            self.lg.log_DHS(dh)
        self.lg.flush_DHS_buffer()
        time.sleep(0.5)  # waiting for thread
        t = len(DHSensorData.read_from_db(self.conn))
        self.assertEqual(k, t-n)
