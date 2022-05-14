import logging
import time

import can

from data_models.base_sensor_data import BaseSensorData


# Base class to be inherited from when creating can connections


class BaseCANConnection:
    def __init__(self, bus_type, channel, bitrate):
        self._timed_out = False
        try:
            self._bus = can.interface.Bus(bustype=bus_type, channel=channel, bitrate=bitrate)
        except can.interfaces.kvaser.CANLIBInitializationError as err:
            logging.error(err)
            self._bus = None
        self.last = False
        self._channel = channel
        self.sensor_data = BaseSensorData()

    def read(self):
        self.last = False
        # reads until the last message in the iteration is received
        while not self.last:
            msg: can.Message = self.read_from_bus()
            if msg is not None:
                # the message_matcher returns true if it receives the last message
                self.last = self.sensor_data.message_mapper(msg)
            else:
                self.last = True

        self.sensor_data.timestamp = time.time()
        self.sensor_data.timed_out = self._timed_out
        return self.sensor_data

    # reads from bus and passes on the message, disables reading if it times out and logs error to stderr
    def read_from_bus(self) -> can.Message:
        if not self._timed_out and self._bus:
            m = self._bus.recv(timeout=2.0)
            if m is None:
                logging.error(f"Reading from CAN channel {self._channel} timed out, reading disabled")
                self._timed_out = True
            return m
        if self._timed_out or not self._bus:
            time.sleep(0.01)
        return None

    # writes an entire ControlData object to the bus
    def send(self, msg_list: list[tuple[int, bytearray]]):
        for msg in msg_list:
            logging.debug(msg)
            m = can.Message(time.time(), arbitration_id=msg[0], data=msg[1], is_extended_id=False)
            self.write_to_bus(m)

    def write_to_bus(self, m: can.Message):
        if not self._timed_out and self._bus:
            try:
                self._bus.send(m, timeout=2)
            except can.interfaces.kvaser.canlib.CANLIBOperationError as err:
                print(err)
                self._timed_out = True
                logging.error(f"Writing to CAN channel {self._channel} timed out, reading disabled")

    def reconnect(self):
        logging.info(f"Reconnecting to CAN channel {self._channel}")
        self._timed_out = False
