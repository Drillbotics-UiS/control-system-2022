from sqlite3 import Row

from can import Message

from data_models.base_sensor_data import BaseSensorData
from data_models.interlock import Interlock
from data_models.weight_on_bit import WeightOnBit
from utility.utils import byte_to_float, byte_to_int


# Class for data that is received from the plc
class PLCSensorData(BaseSensorData):
    def __init__(self):
        super().__init__()

        self.plc_state: int = 0
        self.wob = WeightOnBit()
        self.top_drive_rpm: float = 0.0
        self.top_drive_rpm_set_point = 0.0
        self.top_drive_torque = 0.0
        self.top_drive_torque_set_point = 0.0
        self.pressure_circulation_system: float = 0.0
        self.temp_circulation_system: float = 0.0
        self.interlock = Interlock()
        self.pump_set_point = 0.0
        self.hoisting_height = 0.0

    def write_to_db(self, conn):
        conn.execute(
            "INSERT INTO plc("
            "plc_state,"
            "wob_1, "
            "wob_2, "
            "wob_3, "
            "top_drive_rpm, "
            "top_drive_rpm_set_point, "
            "top_drive_torque, "
            "top_drive_torque_set_point,"
            "pressure_circulation_system, "
            "temp_circulation_system,"
            "interlock,"
            "pump_set_point,"
            "hoisting_height,"
            "timestamp) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (self.plc_state, self.wob.sensor_1, self.wob.sensor_2, self.wob.sensor_3, self.top_drive_rpm,
             self.top_drive_rpm_set_point, self.top_drive_torque, self.top_drive_torque_set_point,
             self.pressure_circulation_system, self.temp_circulation_system, self.interlock.combined_value,
             self.pump_set_point, self.hoisting_height, self.timestamp)
        )

    @staticmethod
    def read_from_db(conn) -> list[Row]:
        rows = conn.execute(
            "SELECT * FROM plc",
        ).fetchall()
        return rows

    def message_mapper(self, msg: Message) -> bool:
        match msg.arbitration_id:
            # TODO fix correct ids in both python and plc code
            case 100:
                self.plc_state = byte_to_int(msg.data[0:4])
            case 110:
                self.wob.sensor_1 = byte_to_float(msg.data[0:4])
                self.wob.sensor_2 = byte_to_float(msg.data[4:8])
            case 120:
                self.wob.sensor_3 = byte_to_float(msg.data[0:4])
                self.wob.sum = byte_to_float(msg.data[4:8])
            case 130:
                self.pressure_circulation_system = byte_to_float(msg.data[0:4])
                self.temp_circulation_system = byte_to_float(msg.data[4:8])
            case 140:
                self.interlock.switch_mapper(byte_to_int(msg.data[0:4]))
            case 150:
                self.pump_set_point = byte_to_float(msg.data[0:4])
                self.hoisting_height = byte_to_float(msg.data[4:8])
            case 160:
                self.top_drive_rpm = byte_to_float(msg.data[0:4])
                self.top_drive_torque = byte_to_float(msg.data[4:8])
            case 170:
                self.top_drive_rpm_set_point = byte_to_float(msg.data[0:4])
                self.top_drive_torque_set_point = byte_to_float(msg.data[4:8])
            case 199:
                return True
        return False
