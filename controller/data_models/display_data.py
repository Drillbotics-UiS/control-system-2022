import time

from data_models.interlock import Interlock
# Class for data is sent to the GUI
from data_models.refresh_rate import RefreshRate
from data_models.tension_log_data import TensionLogData
from data_models.weight_on_bit import WeightOnBit
from data_models.well_log_data import WellLogData


class DisplayData:
    def __init__(self):
        self.top_drive_rpm: float = 0.0
        self.top_drive_torque: float = 0.0
        self.pressure_circulation_system: float = 0.0
        self.temp_circulation_system: float = 0.0
        self.MD: float = 0.0
        self.INC: float = 0.0
        self.AZM: float = 0.0
        self.tension_c1: float = 0.0
        self.tension_c2: float = 0.0
        self.VER_DEV: float = 0.0
        self.flow_rate: float = 0.0
        self.interlock = Interlock()
        self.wob = WeightOnBit()
        self.timestamp: float = time.time()
        self.PLC_CAN_timed_out = False
        self.DHS_CAN_timed_out = False
        self.estimated_position: tuple[float, ...] = (0, 0, 0)
        self.hoisting_height = 0.0
        self.well_log_data = WellLogData()
        self.tension_log_data = TensionLogData()
        self.refresh_rate = RefreshRate()
        self.TVD = 0.0
        self.ROP = 0.0
        self.target_point = None
        self.elapsed_time = 0.0
