import struct
import unittest

from can import Message

from data_models.dh_sensor_data import DHSensorData


class TestDHSensorData(unittest.TestCase):
    # Tests that the values gets mapped with correct id and that only id 399 returns True
    def test_message_matcher(self):
        sensor_data = DHSensorData()
        quat_x = 394.5
        mag_z = -391.4
        acc_y = 12.13
        m = Message()
        m.arbitration_id = 311
        m.data = struct.pack("<f", quat_x)
        last = sensor_data.message_mapper(m)
        self.assertEqual(last, False)
        m.arbitration_id = 322
        m.data = struct.pack("<f", mag_z)
        last = sensor_data.message_mapper(m)
        self.assertEqual(last, False)
        m.arbitration_id = 301
        m.data = struct.pack("<f", acc_y)
        last = sensor_data.message_mapper(m)
        self.assertEqual(last, False)
        m.arbitration_id = 399
        last = sensor_data.message_mapper(m)
        self.assertAlmostEqual(quat_x, sensor_data.quat_x, 3)
        self.assertAlmostEqual(mag_z, sensor_data.mag_z, 3)
        self.assertAlmostEqual(acc_y, sensor_data.acc_y, 3)
        self.assertEqual(last, True)
