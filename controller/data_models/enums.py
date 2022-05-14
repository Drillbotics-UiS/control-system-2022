from enum import IntFlag, Enum


class HoistingDirection(IntFlag):
    UP: int = 1
    DOWN: int = -1


class DoorSensor(IntFlag):
    OPEN: int = 0
    CLOSED: int = 1


class DeviceState(IntFlag):
    ENABLED: int = 1
    DISABLED: int = 0


class LimitSwitch(IntFlag):
    ACTIVE: int = 0
    INACTIVE: int = 1

class IndicatorColor(Enum):
    RED = "rgba(255,0,0,0.8)"
    BLUE = "rgba(0,255,0,0.8)"
    YELLOW = "rgba(255,255,0,0.8)"
    GREEN = "rgba(0,255,0,0.8)"
    WHITE = "rgba(0,0,0,0)"
