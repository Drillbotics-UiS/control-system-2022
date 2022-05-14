from connections.base_can_connection import BaseCANConnection
from data_models.plc_sensor_data import PLCSensorData


class CANPLCConnection(BaseCANConnection):
    def __init__(self, bus_type, channel, bitrate):
        super().__init__(bus_type, channel, bitrate)
        self.sensor_data = PLCSensorData()

    # Just a wrapper for type-hinting
    def read(self) -> PLCSensorData:
        return super().read()
