import math
import random


class TensionLogData:
    def __init__(self,
                 tensionC1=0.0,
                 tensionC2=0.0,
                 depth=0.0):
        self.tensionC1 = tensionC1
        self.tensionC2 = tensionC2
        self.depth = depth

    def populate_randomly(self, depth):
        self.depth = depth
        self.tensionC1 = 0.25 + 0.25 * math.sin(0.01 * depth) + 0.01 * random.randint(0, 1)
        self.tensionC2 = 0.75 + 0.25 * math.cos(0.01 * depth) + 0.01 * random.randint(-1, 0)
