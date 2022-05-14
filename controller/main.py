import json
import logging
from multiprocessing import Queue, Process

from connections.can_dhs_connection import CANDHSConnection
from connections.can_plc_connection import CANPLCConnection
from data_models.user_input import UserInput
from drill_controller.drill_controller import DrillController
from logger.logger import Logger
from qt_gui.main_window import MainWindow
from utility.flow_controller import FlowController

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


class Main:
    def __init__(self, conf):
        # self.plc_ADS_conn = ADSConnection(conf["ams_address"], conf["ams_port"])
        self.PLC_CAN_conn = CANPLCConnection(conf["can_bus_type"], conf["can_channel_plc"], conf["can_bitrate_plc"])
        self.drill_controller = DrillController()

        # Queue for sending data to GUI
        self.display_queue = Queue()

        # Queue for inputs from GUI
        self.user_input_queue = Queue()

        # Queue for receiving statuses from GUI
        self.GUI_management_queue = Queue()

        # Queue for receiving values from DHS
        self.DHS_queue = Queue()

        # Queue for sending signal to reactivate if timed out
        self.DHS_management_queue = Queue()

        self.GUI_process = Process(target=MainWindow.run_gui,
                                   args=(self.display_queue, self.user_input_queue, self.GUI_management_queue, conf))
        self.DHS_process = Process(target=CANDHSConnection.run_dh_sensor, args=(
            conf["can_bus_type"], conf["can_channel_dhs"], conf["can_bitrate_dhs"], self.DHS_queue,
            self.DHS_management_queue))

        self._logger = Logger(conf["schema_file"], conf["log_buffer_size"], conf["logging_speed"])

        self.GUI_flow_controller = FlowController()

    def read_DHS(self):
        # Read from DHS and pass to controller
        if self.DHS_queue.qsize() > 0:
            dhs_data = self.DHS_queue.get()
            self._logger.log_DHS(dhs_data)
            self.drill_controller.dh_sensor_input(dhs_data)

    def read_user_input(self):
        # Read user input if there is any
        if self.user_input_queue.qsize() > 0:
            user_input_data: UserInput = self.user_input_queue.get()
            if user_input_data.CAN_reconnect:
                self.PLC_CAN_conn.reconnect()
                self.DHS_management_queue.put(1)
            self._logger.run_logger = user_input_data.run_auto
            self.drill_controller.receive_user_input(user_input_data)

    def run(self) -> None:
        self.GUI_process.start()
        self.DHS_process.start()
        running = True

        # Send one time to activate plc can communication
        self.PLC_CAN_conn.send(self.drill_controller.get_can_output())

        while running:
            # Read data from PLC and pass to controller
            plc_data = self.PLC_CAN_conn.read()
            self._logger.log_PLC(plc_data)
            self.drill_controller.plc_sensor_input(plc_data)

            self.read_DHS()
            self.read_user_input()

            # Read from management queue for closing program and for controlling update interval
            if self.GUI_management_queue.qsize() > 0:
                msg = self.GUI_management_queue.get()
                if msg == -1:
                    break
                if msg == 1:
                    self.GUI_flow_controller.slow_down()

            if self.GUI_flow_controller.run():
                # Update the GUI when the flow controller allows it
                self.display_queue.put(self.drill_controller.gui_output())

            # Send control data to plc
            self.PLC_CAN_conn.send(self.drill_controller.generate_control_output().get_can_output())

        self.stop()

    def stop(self) -> None:
        self.GUI_process.terminate()
        logging.info("Terminated GUI process")
        self.DHS_process.terminate()
        logging.info("Terminated DHS process")
        self.DHS_queue.close()
        self.DHS_management_queue.close()
        self.display_queue.close()
        self.user_input_queue.close()
        self.GUI_management_queue.close()
        logging.info("Closed queues between GUI and main function")


if __name__ == '__main__':
    configfile = open("config.json")
    config = json.load(configfile)
    configfile.close()
    program = Main(config)
    try:
        program.run()
    except KeyboardInterrupt:
        program.stop()
