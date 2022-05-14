# Class for data that is received from the DHS
from sqlite3 import Row

from can import Message

from data_models.base_sensor_data import BaseSensorData
from utility.utils import byte_to_float


class DHSensorData(BaseSensorData):
    def __init__(self):
        super().__init__()
        self.acc_x: float = 0.0
        self.acc_y: float = 0.0
        self.acc_z: float = 0.0
        self.quat_x: float = 0.0
        self.quat_y: float = 0.0
        self.quat_z: float = 0.0
        self.quat_w: float = 0.0
        self.mag_x: float = 0.0
        self.mag_y: float = 0.0
        self.mag_z: float = 0.0

    def __str__(self):
        return "acc_x\tacc_y\tacc_z\tquat_w\tquat_x\tquat_y\tquat_z\tmag_x\tmag_y\tmag_z\n" + \
               f"{self.acc_x:.2f}\t {self.acc_y:.2f}\t{self.acc_z:.2f}\t{self.quat_w:.2f}\t{self.quat_x:.2f}\t{self.quat_y:.2f}\t{self.quat_z:.2f}\t{self.mag_x:.2f}\t{self.mag_y:.2f}\t{self.mag_z:.2f}"

    def write_to_db(self, conn):
        conn.execute(
            "INSERT INTO dh_sensor("
            "acc_x,"
            "acc_y,"
            "acc_z,"
            "quat_x,"
            "quat_y,"
            "quat_z,"
            "quat_w,"
            "mag_x,"
            "mag_y,"
            "mag_z,"
            "timestamp)"
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                self.acc_x, self.acc_y, self.acc_z,
                self.quat_x, self.quat_y, self.quat_z, self.quat_z,
                self.mag_x, self.mag_z, self.mag_z, self.timestamp
            )
        )

    @staticmethod
    def read_from_db(conn) -> list[Row]:
        rows = conn.execute(
            "SELECT * FROM dh_sensor",
        ).fetchall()
        return rows

    # Writes the value in a can message to the corresponding field in the class
    # Returns true if the message is the last in the sequence
    def message_mapper(self, msg: Message) -> bool:
        match msg.arbitration_id:
            case 300:
                self.acc_x = byte_to_float(msg.data[0:4])
            case 301:
                self.acc_y = byte_to_float(msg.data[0:4])
            case 302:
                self.acc_z = byte_to_float(msg.data[0:4])
            case 310:
                self.quat_w = byte_to_float(msg.data[0:4])
            case 311:
                self.quat_x = byte_to_float(msg.data[0:4])
            case 312:
                self.quat_y = byte_to_float(msg.data[0:4])
            case 313:
                self.quat_z = byte_to_float(msg.data[0:4])
            case 320:
                self.mag_x = byte_to_float(msg.data[0:4])
            case 321:
                self.mag_y = byte_to_float(msg.data[0:4])
            case 322:
                self.mag_z = byte_to_float(msg.data[0:4])
            case 399:
                return True
        return False
