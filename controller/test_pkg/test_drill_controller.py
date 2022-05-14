import unittest

from data_models.user_input import UserInput
from drill_controller.drill_controller import DrillController
from utility.utils import byte_to_float


class TestDrillController(unittest.TestCase):
    def test_manual_input(self):
        controller = DrillController()
        user_input = UserInput()
        user_input.control_mode = 0
        user_input.hoisting_enable = True
        user_input.hoisting_demand_value = 34.5
        controller.receive_user_input(user_input)
        result = controller.generate_control_output().get_can_output()

        # Assertions must be set in the same order as in generate_control_output()
        # in the DrillController class

        # control mode
        self.assertEqual(result[0][1][3], 0)
        self.assertEqual(result[0][0], 200)

        # hoisting value
        self.assertEqual(byte_to_float(result[1][1][4:8]), 34.5)
        self.assertEqual(result[1][0], 202)

        # enable hoisting
        self.assertEqual(result[2][1][3], 1)
        self.assertEqual(result[2][0], 202)
