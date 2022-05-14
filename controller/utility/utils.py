import struct
from os import environ


def suppress_qt_warnings() -> None:
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def byte_to_int(b: bytearray) -> int:
    if len(b) > 4:
        raise ValueError("Cannot use more than 4 bytes for integer")
    return int.from_bytes(b[0:len(b)], "big", signed=True)


def byte_to_float(b: bytearray) -> float:
    return struct.unpack("<f", b)[0]
