import unittest

from data_models.interlock import Interlock


class TestInterLock(unittest.TestCase):
    def test_matcher_all_1(self):
        interlock = Interlock()
        interlock.switch_mapper(255)
        self.assertEqual(1, interlock.front_door)
        self.assertEqual(1, interlock.rear_door)
        self.assertEqual(1, interlock.limit_hoisting_bottom)
        self.assertEqual(1, interlock.limit_hoisting_top)
        self.assertEqual(1, interlock.limit_stabilizer_hoist_side)
        self.assertEqual(1, interlock.limit_stabilizer_opposite_hoist)
        self.assertEqual(1, interlock.hoisting)
        self.assertEqual(1, interlock.pump)

    def test_matcher_all_0(self):
        interlock = Interlock()
        interlock.switch_mapper(256)
        self.assertEqual(0, interlock.front_door)
        self.assertEqual(0, interlock.rear_door)
        self.assertEqual(0, interlock.limit_hoisting_bottom)
        self.assertEqual(0, interlock.limit_hoisting_top)
        self.assertEqual(0, interlock.limit_stabilizer_hoist_side)
        self.assertEqual(0, interlock.limit_stabilizer_opposite_hoist)
        self.assertEqual(0, interlock.hoisting)
        self.assertEqual(0, interlock.pump)

    def test_matcher_mix_1(self):
        interlock = Interlock()
        interlock.switch_mapper(85)
        self.assertEqual(1, interlock.front_door)
        self.assertEqual(0, interlock.rear_door)
        self.assertEqual(1, interlock.limit_hoisting_bottom)
        self.assertEqual(0, interlock.limit_hoisting_top)
        self.assertEqual(1, interlock.limit_stabilizer_hoist_side)
        self.assertEqual(0, interlock.limit_stabilizer_opposite_hoist)
        self.assertEqual(1, interlock.hoisting)
        self.assertEqual(0, interlock.pump)

    def test_matcher_mix_2(self):
        interlock = Interlock()
        interlock.switch_mapper(170)
        self.assertEqual(0, interlock.front_door)
        self.assertEqual(1, interlock.rear_door)
        self.assertEqual(0, interlock.limit_hoisting_bottom)
        self.assertEqual(1, interlock.limit_hoisting_top)
        self.assertEqual(0, interlock.limit_stabilizer_hoist_side)
        self.assertEqual(1, interlock.limit_stabilizer_opposite_hoist)
        self.assertEqual(0, interlock.hoisting)
        self.assertEqual(1, interlock.pump)
