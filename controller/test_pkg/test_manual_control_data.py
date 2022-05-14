import unittest

from data_models.manual_control_data import ManualControlData


class TestManualControlData(unittest.TestCase):
    # sets the same values two times to check if they get included
    def test_num_msg_all(self):
        data = ManualControlData()
        data.pump_open = 1
        data.hoisting_enable = 1
        data.hoisting_demand_value = 20.0
        data.pump_enable = 1
        data.pump_PID = 1
        data.stabilizer_homing = 1
        data.stabilizer_actuator = (30.2, 1)
        data.top_drive_rpm_set_point = 30.0
        data.top_drive_torque_set_point = 21.0
        data.top_drive_enable = 1
        self.assertEqual(len(data.to_can()), 10)
        self.assertEqual(len(data.to_can()), 0)
        data.pump_open = 1
        data.hoisting_enable = 1
        data.hoisting_demand_value = 20.0
        data.pump_enable = 1
        data.pump_PID = 1
        data.stabilizer_homing = 1
        data.stabilizer_actuator = (30.2, 1)
        data.top_drive_rpm_set_point = 30.0
        data.top_drive_torque_set_point = 21.0
        data.top_drive_enable = 1
        self.assertEqual(len(data.to_can()), 0)

    def test_num_msg_some(self):
        data = ManualControlData()
        data.pump_open = 1
        data.hoisting_enable = 1
        data.hoisting_demand_value = 334.1
        self.assertEqual(len(data.to_can()), 3)

    # Checks that the msg ids arrive in the order they were changed
    def test_msg_id(self):
        data = ManualControlData()
        data.stabilizer_homing = 1
        data.hoisting_demand_value = 20.0
        data.pump_enable = 1
        data.pump_PID = 1
        values = data.to_can()
        self.assertEqual(values[0][0], 204)
        self.assertEqual(values[1][0], 202)
        self.assertEqual(values[2][0], 203)
        self.assertEqual(values[3][0], 203)
