
import os
import random
import sys
import json
from sqlite3 import connect
from time import sleep
import time

from logger.logger import Logger
from data_models.dh_sensor_data import DHSensorData


def main():
    if len(sys.argv) != 3:
        print("ERROR: the script requires 2 arguments: frequency (messages per s) and duration (s, h or m).")
        print("example: py test_db.py 20 1m")
        sys.exit(1)
    if not sys.argv[1].isdigit():
        print("ERROR: frequency argument must be an integer.")
        sys.exit(1)
    if not sys.argv[2][-1] in "smh" or not sys.argv[2][:-1].isdigit():
        print("ERROR: duration must be specified as an integer and either s, m or h.")
        sys.exit(1)
    
    
    
    frequency = int(sys.argv[1])
    time_conversion_dict = {
        "s": 1,
        "m": 60,
        "h": 3600,
    }
    seconds = int(sys.argv[2][:-1])*time_conversion_dict[sys.argv[2][-1]]

    configfile = open("config.json")
    config = json.load(configfile)
    configfile.close()
    lg = Logger(config["log_buffer_size"], config["log_file"])
    conn = connect(lg.filename)

    if conn is None:
        print("ERROR: couldn't connect to db.")
        sys.exit(1)
    
    with open(os.path.join("logger", "schema.sql")) as file:
        conn.executescript(file.read())
        conn.commit()

    s, = conn.execute("SELECT COUNT(did) FROM dh_sensor").fetchone()
    messages_count = frequency * seconds

    start_time = time.time()
    wanted_end_time = time.time() + seconds
    for i in range(messages_count):
        lg.log_DHS(generate_dh_data())
        time.sleep(max(0, (wanted_end_time - time.time())/(messages_count - i)))

    n = 0
    while n-s != messages_count:
        end_time = time.time()
        time.sleep(0.5)
        n, = conn.execute("SELECT COUNT(did) FROM dh_sensor").fetchone()
        print(f"logged {n-s} entries in {end_time-start_time:.2f} seconds.")


def generate_dh_data():
    dh = DHSensorData()
    dh.acc_x = random.random()
    dh.acc_y = random.random()
    dh.acc_z = random.random()
    dh.quat_x = random.random()
    dh.quat_y = random.random()
    dh.quat_z = random.random()
    dh.quat_w = random.random()
    dh.mag_x = random.random()
    dh.mag_y = random.random()
    dh.mag_z = random.random()
    return dh



    

    

if __name__ == "__main__":
    main()
