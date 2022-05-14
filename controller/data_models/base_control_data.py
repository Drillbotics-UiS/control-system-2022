import struct


# Base class for data that is sent to the plc
class BaseControlData:
    def __init__(self):
        self._control_mode: int = 1
        self._can_list = []

    @property
    def control_mode(self):
        return self._control_mode

    @control_mode.setter
    def control_mode(self, value):
        if self._control_mode != value:
            self._control_mode = value
            a = bytearray(8)
            self.write_int_to_byte_array(a, self.control_mode, 0)
            self._can_list.append((200, a))

    # Creates a new message list and returns the old one
    def to_can(self) -> list[tuple[int, bytearray]]:
        values = self._can_list
        self._can_list: list[(int, bytearray)] = []
        return values

    @staticmethod
    def write_int_to_byte_array(b: bytearray, val: int, pos: int):
        b[pos:pos + 4] = struct.pack(">i", val)

    @staticmethod
    def write_float_to_byte_array(b: bytearray, val: float, pos: int):
        b[pos:pos + 4] = struct.pack("<f", val)
