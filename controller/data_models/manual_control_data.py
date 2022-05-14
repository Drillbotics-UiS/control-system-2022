from data_models.base_control_data import BaseControlData


# The ManualControlData class will detect changes in the properties and stage
# a message for sending, this is so only one message gets sent per event,
# for example when activating the hoisting
class ManualControlData(BaseControlData):
    def __init__(self):
        super().__init__()

        # 201
        self._pump_open: int = 0

        # 202
        self._hoisting_enable: int = 0
        self._hoisting_demand_value: float = 0.0

        # 203
        self._pump_enable: int = 0
        self._pump_PID: float = 0.0

        # 204
        self._stabilizer_homing: int = 0

        # 205
        self._stabilizer_actuator: tuple[float, int] = (0.0, 0)

        # 206
        self._top_drive_rpm_set_point: float = 0.0
        self._top_drive_torque_set_point: float = 0.0

        # 207
        # self._RSS_actuator

        # 208
        self._top_drive_enable: int = 0

    @property
    def pump_open(self):
        return self._pump_open

    @pump_open.setter
    def pump_open(self, value):
        if self._pump_open != value:
            self._pump_open = value
            a = bytearray(8)
            self.write_int_to_byte_array(a, self._pump_open, 0)
            self._can_list.append((201, a))

    @property
    def hoisting_enable(self):
        return self._hoisting_enable

    @hoisting_enable.setter
    def hoisting_enable(self, value):
        if self._hoisting_enable != value:
            self._hoisting_enable = value
            a = bytearray(8)
            self.write_int_to_byte_array(a, self._hoisting_enable, 0)
            self.write_float_to_byte_array(a, self._hoisting_demand_value, 4)
            self._can_list.append((202, a))

    @property
    def hoisting_demand_value(self):
        return self._hoisting_demand_value

    @hoisting_demand_value.setter
    def hoisting_demand_value(self, value):
        if self._hoisting_demand_value != value:
            self._hoisting_demand_value = value
            a = bytearray(8)
            self.write_int_to_byte_array(a, self._hoisting_enable, 0)
            self.write_float_to_byte_array(a, self._hoisting_demand_value, 4)
            self._can_list.append((202, a))

    @property
    def pump_enable(self):
        return self._pump_enable

    @pump_enable.setter
    def pump_enable(self, value):
        if self._pump_enable != value:
            self._pump_enable = value
            a = bytearray(8)
            self.write_int_to_byte_array(a, self._pump_enable, 0)
            self.write_float_to_byte_array(a, self._pump_PID, 4)
            self._can_list.append((203, a))

    @property
    def pump_PID(self):
        return self._pump_PID

    @pump_PID.setter
    def pump_PID(self, value):
        if self._pump_PID != value:
            self._pump_PID = value
            a = bytearray(8)
            self.write_int_to_byte_array(a, self._pump_enable, 0)
            self.write_float_to_byte_array(a, self._pump_PID, 4)
            self._can_list.append((203, a))

    @property
    def stabilizer_homing(self):
        return self._stabilizer_homing

    @stabilizer_homing.setter
    def stabilizer_homing(self, value):
        if self._stabilizer_homing != value:
            self._stabilizer_homing = value
            a = bytearray(8)
            self.write_int_to_byte_array(a, self._stabilizer_homing, 0)
            self._can_list.append((204, a))

    @property
    def stabilizer_actuator(self):
        return self._stabilizer_actuator

    @stabilizer_actuator.setter
    def stabilizer_actuator(self, value):
        if self._stabilizer_actuator != value:
            self._stabilizer_actuator = value
            a = bytearray(8)
            self.write_float_to_byte_array(a, self._stabilizer_actuator[0], 0)
            self.write_int_to_byte_array(a, self._stabilizer_actuator[1], 4)
            self._can_list.append((205, a))

    @property
    def top_drive_rpm_set_point(self):
        return self._top_drive_rpm_set_point

    @top_drive_rpm_set_point.setter
    def top_drive_rpm_set_point(self, value):
        if self._top_drive_rpm_set_point != value:
            self._top_drive_rpm_set_point = value
            a = bytearray(8)
            self.write_float_to_byte_array(a, self._top_drive_rpm_set_point, 0)
            self.write_float_to_byte_array(a, self._top_drive_torque_set_point, 4)
            self._can_list.append((206, a))

    @property
    def top_drive_torque_set_point(self):
        return self._top_drive_torque_set_point

    @top_drive_torque_set_point.setter
    def top_drive_torque_set_point(self, value):
        if self._top_drive_torque_set_point != value:
            self._top_drive_torque_set_point = value
            a = bytearray(8)
            self.write_float_to_byte_array(a, self._top_drive_rpm_set_point, 0)
            self.write_float_to_byte_array(a, self._top_drive_torque_set_point, 4)
            self._can_list.append((206, a))

    @property
    def top_drive_enable(self):
        return self._top_drive_enable

    @top_drive_enable.setter
    def top_drive_enable(self, value):
        if self._top_drive_enable != value:
            self._top_drive_enable = value
            a = bytearray(8)
            self.write_int_to_byte_array(a, self._top_drive_enable, 0)
            self._can_list.append((208, a))
