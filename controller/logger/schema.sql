--DROP TABLE IF EXISTS measurement;
--DROP TABLE IF EXISTS dh_sensor;
--DROP TABLE IF EXISTS user_input;

CREATE TABLE IF NOT EXISTS plc
(
    pid INTEGER PRIMARY KEY AUTOINCREMENT,
    plc_state INTEGER,
    wob_1 INTEGER,
    wob_2 INTEGER,
    wob_3 INTEGER,
    top_drive_rpm REAL,
    top_drive_rpm_set_point REAL,
    top_drive_torque REAL,
    top_drive_torque_set_point REAL,
    pressure_circulation_system REAL,
    temp_circulation_system REAL,
    interlock INTEGER,
    pump_set_point REAL,
    hoisting_height REAL,
    timestamp REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS dh_sensor
(
    did INTEGER PRIMARY KEY AUTOINCREMENT,
    acc_x REAL,
    acc_y REAL,
    acc_z REAL,
    quat_x REAL,
    quat_y REAL,
    quat_z REAL,
    quat_w REAL,
    mag_x REAL,
    mag_y REAL,
    mag_z REAL,
    timestamp REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS user_input
(
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    force_send INTEGER,
    CAN_reconnect INTEGER,
    control_mode INTEGER,
    hoisting_enable INTEGER,
    hoisting_demand_value REAL,
    pump_enable INTEGER,
    pump_PID REAL,
    pump_open INTEGER,
    top_drive_enable INTEGER,
    top_drive_rpm_set_point REAL,
    top_drive_torque_set_point REAL,
    timestamp TEXT NOT NULL
);