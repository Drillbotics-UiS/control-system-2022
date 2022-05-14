from multiprocessing import Queue
from connections.base_can_connection import BaseCANConnection
from data_models.dh_sensor_data import DHSensorData


class CANDHSConnection(BaseCANConnection):
    def __init__(self, bus_type, channel, bitrate):
        super().__init__(bus_type, channel, bitrate)
        self.sensor_data = DHSensorData()

    # Just a wrapper for type-hinting
    def read(self) -> DHSensorData:
        return super().read()

    @staticmethod
    def run_dh_sensor(bus_type, channel, bitrate, output_queue: Queue, recv_queue : Queue):
        conn = CANDHSConnection(bus_type, channel, bitrate)
        while True:
            if recv_queue.qsize() > 0:
                recv_queue.get()
                conn.reconnect()
            output_queue.put(conn.read())
