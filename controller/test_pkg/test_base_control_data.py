import unittest

from data_models.base_control_data import BaseControlData


class TestBaseControlData(unittest.TestCase):
    def test_return_type(self):
        c_data = BaseControlData()
        c_data.rpm = 120
        c_data.torque = 144
        can_data = c_data.to_can()
        self.assertEqual(type(can_data), list)

    def test_write_float_to_byte_array_small_number(self):
        b_arr = bytearray(8)
        BaseControlData.write_float_to_byte_array(b_arr, 50, 4)
        self.assertEqual(b_arr[6], 72)
        self.assertEqual(b_arr[7], 66)

    def test_write_negative_float_to_byte_array_small_number(self):
        b_arr = bytearray(8)
        BaseControlData.write_float_to_byte_array(b_arr, -50, 4)
        self.assertEqual(b_arr[6], 72)
        self.assertEqual(b_arr[7], 194)

    def test_write_int_to_byte_array_small_number(self):
        b_arr = bytearray(8)
        BaseControlData.write_int_to_byte_array(b_arr, 50, 4)
        self.assertEqual(b_arr[7], 50)

    def test_write_negative_int_to_byte_array_small_number(self):
        b_arr = bytearray(8)
        BaseControlData.write_int_to_byte_array(b_arr, -50, 4)
        self.assertEqual(b_arr[7], 255 - 50 + 1)

    def test_write_int_to_byte_array_large_number(self):
        b_arr = bytearray(8)
        BaseControlData.write_int_to_byte_array(b_arr, 2117482627, 0)
        self.assertEqual(b_arr[0], 126)
        self.assertEqual(b_arr[1], 54)
        self.assertEqual(b_arr[2], 56)
        self.assertEqual(b_arr[3], 131)

    def test_write_negative_int_to_byte_array_large_number(self):
        b_arr = bytearray(8)
        BaseControlData.write_int_to_byte_array(b_arr, -2117482752, 0)
        self.assertEqual(b_arr[0], 129)
        self.assertEqual(b_arr[1], 201)
        self.assertEqual(b_arr[2], 199)
        self.assertEqual(b_arr[3], 0)
