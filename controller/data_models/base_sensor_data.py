import time

from can import Message


class BaseSensorData:
    def __init__(self):
        self.timestamp = time.time()

        self.timed_out = False

    def message_mapper(self, msg: Message):
        pass
