import logging

import pyads

from connections.ads_read_writer import ADSReadWriter


class ADSConnection:
    def __init__(self, ams_address, ams_port):
        self.plc_connection = pyads.Connection(ams_address, ams_port)
        self.plc_connection.open()
        self.plc = ADSReadWriter(self.plc_connection)

    def __del__(self):
        self.plc_connection.close()
        logging.info("ADS connection closed")

    def __str__(self):
        return f"PLC is connected {self.plc_connection.is_open}\nIP-Address: {self.plc_connection.ip_address}"

    @property
    def ip_address(self) -> str:
        if self.plc_connection:
            return f"IP Address: {self.plc_connection.ip_address}"

    @property
    def device_status(self) -> str:
        if self.plc_connection and self.plc_connection.is_open:
            return "Device Status: Online"
        return "Device Status: Offline"
