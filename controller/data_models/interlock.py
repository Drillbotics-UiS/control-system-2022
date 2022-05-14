from data_models.enums import DoorSensor, DeviceState, LimitSwitch


class Interlock:
    def __init__(self):
        self.front_door: int = DoorSensor.CLOSED
        self.rear_door: int = DoorSensor.CLOSED
        self.limit_hoisting_bottom: int = LimitSwitch.INACTIVE
        self.limit_hoisting_top: int = LimitSwitch.INACTIVE
        self.limit_stabilizer_hoist_side: int = LimitSwitch.INACTIVE
        self.limit_stabilizer_opposite_hoist: int = LimitSwitch.INACTIVE
        self.hoisting: int = DeviceState.DISABLED
        self.pump: int = DeviceState.DISABLED
        self._combined_value: int = 0

    def switch_mapper(self, switch_values: int):
        self._combined_value = switch_values
        self.front_door = switch_values & 1
        self.rear_door = (switch_values & 2) >> 1
        self.limit_hoisting_bottom = (switch_values & 4) >> 2
        self.limit_hoisting_top = (switch_values & 8) >> 3
        self.limit_stabilizer_hoist_side = (switch_values & 16) >> 4
        self.limit_stabilizer_opposite_hoist = (switch_values & 32) >> 5
        self.hoisting = (switch_values & 64) >> 6
        self.pump = (switch_values & 128) >> 7

    @property
    def combined_value(self):
        return self._combined_value
