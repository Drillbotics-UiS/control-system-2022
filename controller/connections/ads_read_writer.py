import logging

import pyads


# this class will take a plc connection as an argument, and you will
# then be able to read and write to the variables on the plc
class ADSReadWriter:
    def __init__(self, plc: pyads.Connection):
        self._plc = plc
        self.connected = True

    @property
    def numeric_value(self) -> int:
        if self.connected:
            try:
                return self._plc.read_by_name('MAIN.numeric_value', pyads.PLCTYPE_DINT)
            except pyads.ADSError or AttributeError:
                logging.error("Cannot access PLC over pyads")
                self.connected = False
            except AttributeError:
                logging.error("Cannot access PLC over pyads")
                self.connected = False
        return 0

    @property
    def multiplier(self) -> int:
        if self.connected:
            try:
                return self._plc.read_by_name('MAIN.multiplier', pyads.PLCTYPE_DINT)
            except pyads.ADSError or AttributeError:
                logging.error("Cannot access PLC over pyads")
                self.connected = False
            except AttributeError:
                logging.error("Cannot access PLC over pyads")
                self.connected = False
        return 0

    @multiplier.setter
    def multiplier(self, value: int):
        if self.connected:
            try:
                self._plc.write_by_name('MAIN.multiplier', value, pyads.PLCTYPE_DINT)
            except pyads.ADSError:
                logging.error("Cannot access PLC over pyads")
                self.connected = False
            except AttributeError:
                logging.error("Cannot access PLC over pyads")
                self.connected = False
