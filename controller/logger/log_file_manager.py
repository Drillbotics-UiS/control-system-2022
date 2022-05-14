import logging
import os
from sqlite3 import connect, Row

from data_models.dh_sensor_data import DHSensorData
from data_models.plc_sensor_data import PLCSensorData
from logger.csv_exporter import write_db_rows


class LogFileManager():
    def __init__(self):
        self.log_filenames = []
        self.__get_log_filenames()

    def delete_file(self, filename: str):
        file = os.path.join("logger", "log", filename)
        logging.info(f"deleting {filename}")
        os.remove(file)

    def export_file(self, filename: str):
        conn = connect(os.path.join("logger", "log", filename))
        conn.row_factory = Row
        dhs_rows = DHSensorData.read_from_db(conn)
        if len(dhs_rows) > 0:
            write_db_rows(os.path.join("logger", "export", os.path.splitext(filename)[0] + "_dhs" + ".csv"),
                          dhs_rows[0].keys(), dhs_rows)

        plc_rows = PLCSensorData.read_from_db(conn)
        if len(plc_rows) > 0:
            write_db_rows(os.path.join("logger", "export", os.path.splitext(filename)[0] + "_plc" + ".csv"),
                          plc_rows[0].keys(), plc_rows)

    # Finds the files with .db file-extension
    def __get_log_filenames(self):
        for filename in os.listdir(os.path.join("logger", "log")):
            if os.path.splitext(filename)[-1] == ".db":
                self.log_filenames.append(filename)

    def update_filenames(self):
        self.log_filenames = []
        self.__get_log_filenames()
