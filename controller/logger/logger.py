import copy
import logging
import os
import threading
import time
from sqlite3 import connect, OperationalError

from data_models.dh_sensor_data import DHSensorData
from data_models.plc_sensor_data import PLCSensorData
from data_models.user_input import UserInput


class Logger:
    def __init__(self, schema_file: str, buff_size: int, logging_speed: int):
        self._schema_file = schema_file
        self._logging_speed = logging_speed
        self._PLC_counter = 1
        self._DHS_counter = 1
        self.filename: str = os.path.join("logger", "log", time.strftime("%Y-%m-%d_%H-%M-%S") + ".db")
        self.buff_size = buff_size
        self._PLC_buffer: list[PLCSensorData] = []
        self._DHS_buffer: list[DHSensorData] = []
        self._run_logger = False

    @property
    def run_logger(self):
        return self._run_logger

    @run_logger.setter
    def run_logger(self, value):
        if value == self._run_logger:
            return

        # Creates the log file when the logger starts running
        if value:
            self.filename = os.path.join("logger", "log", time.strftime("%Y-%m-%d_%H-%M-%S") + ".db")
            self.setup(self.filename, self._schema_file)

        # Flushes buffer when the logger stops logging
        else:
            self.flush_DHS_buffer()
            self.flush_PLC_buffer()
        self._run_logger = value



    # Adds a new value to the buffer, writes to disk if "full"
    def log_PLC(self, item: PLCSensorData):
        if not self._run_logger:
            return
        if self._PLC_counter >= self._logging_speed:
            self._PLC_counter = 0
            self._PLC_buffer.append(copy.copy(item))
            if len(self._PLC_buffer) >= self.buff_size:
                self.flush_PLC_buffer()

        self._PLC_counter += 1

    def log_DHS(self, item: DHSensorData):
        if not self._run_logger:
            return
        if self._DHS_counter >= self._logging_speed:
            self._DHS_counter = 0
            self._DHS_buffer.append(item)
            if len(self._DHS_buffer) >= self.buff_size:
                self.flush_DHS_buffer()

        self._DHS_counter += 1

    def log_user_input(self, item: UserInput):
        t = threading.Thread(target=self.write_to_db, args=((item,), self.filename))
        t.start()

    # Creates a copy of shallow copy of the buffer and creates a new buffer
    # A thread is started to write the buffer to db
    def flush_PLC_buffer(self):
        values = self._PLC_buffer
        self._PLC_buffer = []
        t = threading.Thread(target=self.write_to_db, args=(values, self.filename))
        t.start()

    def flush_DHS_buffer(self):
        values = self._DHS_buffer
        self._DHS_buffer = []
        t = threading.Thread(target=self.write_to_db, args=(values, self.filename))
        t.start()

    # These functions are spawned by the Logger to write to the db

    @staticmethod
    def write_to_db(values: list, filename: str):
        try:
            conn = connect(filename)
            for value in values:
                value.write_to_db(conn)
            conn.commit()
            conn.close()
        except OperationalError as e:
            logging.error("Database cannot sustain logging speed")
            logging.error(e)

    @staticmethod
    # For creating database
    def setup(db_file, schema_file):
        conn = connect(db_file)
        if conn is not None:
            with open(os.path.join("logger", schema_file)) as file:
                conn.executescript(file.read())
                conn.commit()
        conn.close()
