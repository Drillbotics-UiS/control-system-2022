import math
import random


class WellLogData:
    def __init__(self,
                 rop=0.0,
                 wob=0.0,
                 torque=0.0,
                 pump_pressure=0.0,
                 mse=0.0,
                 depth=0.0):
        self.rop = rop
        self.wob = wob
        self.torque = torque
        self.pump_pressure = pump_pressure
        self.mse = mse
        self.depth = depth

    def populate_randomly(self, depth):
        self.depth = depth
        self.rop = 0.5 + 0.3 * math.sin(0.01 * depth) + 0.01 * random.randint(-1, 1)
        self.wob = 0.5 + 0.3 * math.cos(0.01 * depth) + 0.01 * random.randint(-1, 1)
        self.torque = 0.4 + 0.4 * math.sin(0.01 * depth) + 0.01 * random.randint(-1, 1)
        self.pump_pressure = 0.4 + 0.3 * math.cos(0.01 * depth) + 0.01 * random.randint(-1, 1)
        self.mse = 0.6 + 0.2 * math.sin(0.01 * depth) + 0.01 * random.randint(-1, 1)
