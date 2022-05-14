import logging

import numpy


class PlotPath3d:
    def __init__(self, buffsize=2):
        self.x = numpy.empty(buffsize)
        self.x[:] = numpy.nan
        self.y = numpy.empty(buffsize)
        self.y[:] = numpy.nan
        self.z = numpy.empty(buffsize)
        self.z[:] = numpy.nan
        self.index = 0

    def add_point(self, x, y, z):
        self.x[self.index] = x
        self.y[self.index] = y
        self.z[self.index] = z

        self.index += 1

        if self.index == len(self.x):
            self.__expand_arrays()

    def __expand_arrays(self):
        old_size = len(self.x)
        new_size = old_size * 2
        logging.info(f"Expanded array to {new_size} elements")
        self.x = numpy.resize(self.x, new_size)
        self.y = numpy.resize(self.y, new_size)
        self.z = numpy.resize(self.z, new_size)
        self.x[old_size:] = numpy.nan
        self.y[old_size:] = numpy.nan
        self.z[old_size:] = numpy.nan
