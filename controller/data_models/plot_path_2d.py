import logging

import numpy


class PlotPath2d:
    def __init__(self, buffsize=2):
        self.x = numpy.empty(buffsize)
        self.x[:] = numpy.nan
        self.y = numpy.empty(buffsize)
        self.y[:] = numpy.nan
        self.index = 0

    def add_point(self, x, y):
        self.x[self.index] = x
        self.y[self.index] = y

        self.index += 1

        if self.index == len(self.x):
            self.__expand_arrays()

    def __expand_arrays(self):
        old_size = len(self.x)
        new_size = old_size * 2
        self.x = numpy.resize(self.x, new_size)
        self.y = numpy.resize(self.y, new_size)
        self.x[old_size:] = numpy.nan
        self.y[old_size:] = numpy.nan
        logging.info(f"Expanded array to {new_size} elements")
