import copy
import multiprocessing as mp

import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThreadPool, pyqtSignal, QSizeF
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton

from data_models.display_data import DisplayData
from data_models.enums import IndicatorColor, DoorSensor, LimitSwitch
from data_models.interlock import Interlock
from data_models.path_models import MinimumCurvaturePath, SafetyMarginSurface
from data_models.user_input import UserInput
from logger.log_file_manager import LogFileManager
from qt_gui.indicator_LED import IndicatorLED
from qt_gui.interface import Ui_MainWindow
from qt_gui.level_bar import LevelBar
from qt_gui.log_list_item import LogListItem
from qt_gui.plotter_3D import Plotter3D
from qt_gui.well_log import WellLog
from qt_threads.worker import Worker
from utility.utils import suppress_qt_warnings


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, display_queue, input_queue, GUI_management_queue, conf, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self._conf = conf
        plt.style.use(self._conf["plot_style"])
        self.display_queue: mp.Queue = display_queue
        self.input_queue: mp.Queue = input_queue
        self.GUI_management_queue: mp.Queue = GUI_management_queue
        self.setupUi(self)
        if self._conf["program_theme"] == "dark":
            self.set_dark_theme()
        self.running = True
        self.log_file_manager = LogFileManager()
        self.log_list_items = []
        self.add_statusbar_elements()
        # self.base_gv_scale = 1.25
        self.initial_gv_size = None
        self.add_interlock_elements()
        self.add_level_bars()
        self.add_log_list()
        self.inputs = UserInput()
        self.set_input_actions()
        self.add_graphics_view()
        self.update_finished = True
        plt.ion()
        self.show()
        self.threadpool = QThreadPool()
        self.add_initial_threads()
        self.safety_margin_surface_added = False

    # override
    def resizeEvent(self, event):
        self.plotter3d.resize(QSizeF(self.graphicsView.size()))
        self.well_log.resize(QSizeF(self.well_log_view.size()))
        self.tension_log.resize(QSizeF(self.graphicsView_2.size()))
        QtWidgets.QMainWindow.resizeEvent(self, event)

    def add_statusbar_elements(self):
        font = QFont()
        font.setPointSize(10)
        self.CAN_PLC_status_text = QLabel()
        self.CAN_PLC_status_indicator = IndicatorLED()
        self.CAN_PLC_status_text.setText(" PLC CAN: ")
        self.CAN_PLC_status_text.setFont(font)
        self.statusbar.addWidget(self.CAN_PLC_status_text)
        self.statusbar.addWidget(self.CAN_PLC_status_indicator)

        self.CAN_DHS_status_text = QLabel()
        self.CAN_DHS_status_indicator = IndicatorLED()
        self.CAN_DHS_status_text.setText(" DHS CAN: ")
        self.CAN_DHS_status_text.setFont(font)
        self.statusbar.addWidget(self.CAN_DHS_status_text)
        self.statusbar.addWidget(self.CAN_DHS_status_indicator)

        self.reconnect_button = QPushButton()
        self.reconnect_button.setText("Reconnect")
        self.reconnect_button.setFont(font)
        self.reconnect_button.clicked.connect(self.CAN_reconnect)
        self.statusbar.addWidget(self.reconnect_button)

        self.DHS_refresh_rate = QLabel()
        self.DHS_refresh_rate.setFont(font)
        self.statusbar.addWidget(self.DHS_refresh_rate)

        self.PLC_refresh_rate = QLabel()
        self.PLC_refresh_rate.setFont(font)
        self.statusbar.addWidget(self.PLC_refresh_rate)

        self.statusbar.setFont(font)
        self.GUI_refresh_rate = QLabel()
        self.GUI_refresh_rate.setFont(font)
        self.statusbar.addWidget(self.GUI_refresh_rate)

    def add_log_list(self):
        for filename in self.log_file_manager.log_filenames:
            self.log_list.addLayout(LogListItem(self.log_file_manager, filename))

    def update_log_list(self):
        self.log_file_manager.update_filenames()
        for i in range(len(self.log_list)):
            self.log_list.itemAt(i).deleteLater()
        for filename in self.log_file_manager.log_filenames:
            self.log_list.addLayout(LogListItem(self.log_file_manager, filename))

    # Creates and adds the color indicators for the interlocks and limitswitches
    def add_interlock_elements(self):
        self.front_door = IndicatorLED()
        self.rear_door = IndicatorLED()
        self.limit_hoisting_bottom = IndicatorLED()
        self.limit_hoisting_top = IndicatorLED()
        self.limit_stablizer_hoist_side = IndicatorLED()
        self.limit_stablizer_opposite_hoist = IndicatorLED()

        self.interlock_grid.addWidget(self.front_door, 0, 1, 1, 1)
        self.interlock_grid.addWidget(self.rear_door, 1, 1, 1, 1)
        self.interlock_grid.addWidget(self.limit_hoisting_bottom, 2, 1, 1, 1)
        self.interlock_grid.addWidget(self.limit_hoisting_top, 3, 1, 1, 1)
        self.interlock_grid.addWidget(self.limit_stablizer_hoist_side, 4, 1, 1, 1)
        self.interlock_grid.addWidget(self.limit_stablizer_opposite_hoist, 5, 1, 1, 1)

    def add_level_bars(self):
        self.WOB_bar.close()
        self.WOB_bar = LevelBar(2000, 1000, 1600)
        self.WOB_bar.setValue(25)
        self.WOB_layout.insertWidget(0, self.WOB_bar)
        self.torque_bar.close()
        self.torque_bar = LevelBar(100, 40, 70)
        self.torque_bar.setValue(78)
        self.torque_layout.insertWidget(0, self.torque_bar)
        self.pressure_bar.close()
        self.pressure_bar = LevelBar(100, 40, 70)
        self.pressure_bar.setValue(65)
        self.pressure_layout.insertWidget(0, self.pressure_bar)

    def add_graphics_view(self):
        # self.plotter3d = Plotter3D()
        self.plotter3d = Plotter3D(self._conf["plot_background_color"])
        self.graphicsView.setScene(self.plotter3d)

        self.well_log = WellLog((
            ("r", "ROP"),
            ("g", "WOB"),
            ("b", "Torque"),
            ("c", "Pump pressure"),
            ("m", "MSE"),
        ), self._conf["plot_background_color"])
        self.well_log_view.setScene(self.well_log)

        self.tension_log = WellLog((
            ("r", "Tension C1"),
            ("g", "Tension C2"),
        ), self._conf["plot_background_color"])
        self.graphicsView_2.setScene(self.tension_log)
        # self.test_plot = TestView()
        # self.graphicsView_2.setScene(self.test_plot)

    def set_dark_theme(self):
        self.setStyleSheet(
            "QTabBar::tab{background:  #666666;color: white;}"
            "QTabBar::tab:selected {background: #222222;}"
            "QWidget{background: #444444;color: white;}"
        )

    def update_ui(self, n: DisplayData):
        # Does not try to update if it hasn't returned the last emit.
        if not self.update_finished:
            self.GUI_management_queue.put(1)
            return
        self.update_finished = False

        if not self.safety_margin_surface_added:
            mcp = MinimumCurvaturePath((0, 0, 0), n.target_point, random_walk_radius_range=(0, 0))

            sms = SafetyMarginSurface(mcp, 3)
            self.plotter3d.plot_safety_margin_surface(sms)

            self.safety_margin_surface_added = True

        self.top_drive_rpm.setText(str(n.top_drive_rpm))
        self.pressure_circulation_system.setText(f"{n.pressure_circulation_system:.3f} Bar")
        self.wob_sum.setText(f"{n.wob.sum:.3f} N")
        self.pressure_bar.setValue(int(n.pressure_circulation_system))
        self.WOB_bar.setValue(abs(int(n.wob.sum)))
        self.temp_circulation_system.setText(f"{n.temp_circulation_system:.2f} C")
        self.update_interlocks(n.interlock)
        self.update_conn_status(n.PLC_CAN_timed_out, n.DHS_CAN_timed_out)
        self.elapsed_time.setText(f"Timer {n.elapsed_time:.1f} s")
        self.pump_pressure.setText(f"{n.pressure_circulation_system:.4f}")
        self.hoisting_height.setText(f"{n.hoisting_height:.4f} mm")
        self.bit_depth.setText(f"{n.hoisting_height:.4f} mm")
        self.TVD.setText(f"{n.TVD:.2f}")
        self.ROP.setText(f"{n.ROP:.3f} mm/s")
        self.top_drive_torque.setText(f"{n.top_drive_torque:.2f} N")
        self.MD.setText(f"{n.MD:.2f}")
        self.INC.setText(f"{n.MD:.2f}")
        self.AZM.setText(f"{n.AZM:.2f}")
        self.tension_c1.setText(f"{n.tension_c1:.3f} N")
        self.tension_c2.setText(f"{n.tension_c2:.3f} N")
        self.VER_DEV.setText(f"{n.VER_DEV:.3f}")
        self.flow_rate.setText(f"{n.flow_rate:.3f} m^3 / h")
        # self.plotter3d.add_points_to_draw_buffer(n.new_points)
        # self.plotter3d.set_red_line(n.red_line_points)

        self.plotter3d.update_plot(*n.estimated_position)
        # self.plotter3d.update_plot(self.plotter3d.drill_path.index * 0.05, self.plotter3d.drill_path.index * 0.05,
        #                           self.plotter3d.drill_path.index * 0.05)

        self.well_log.update_plot((n.well_log_data.rop, n.well_log_data.wob, n.well_log_data.torque,
                                   n.well_log_data.pump_pressure, n.well_log_data.mse), n.well_log_data.depth)
        self.tension_log.update_plot((n.tension_log_data.tensionC1, n.tension_log_data.tensionC2),
                                     n.tension_log_data.depth)

        self.DHS_refresh_rate.setText(f" DHS: {n.refresh_rate.DHS:.2f} Hz ")
        self.PLC_refresh_rate.setText(f" PLC: {n.refresh_rate.PLC:.2f} Hz ")
        self.GUI_refresh_rate.setText(f" GUI: {n.refresh_rate.GUI:.2f} Hz ")

        self.update_finished = True

    def update_conn_status(self, PLC, DHS):
        if PLC:
            self.CAN_PLC_status_indicator.color = IndicatorColor.YELLOW
        else:
            self.CAN_PLC_status_indicator.color = IndicatorColor.GREEN
        if DHS:
            self.CAN_DHS_status_indicator.color = IndicatorColor.YELLOW
        else:
            self.CAN_DHS_status_indicator.color = IndicatorColor.GREEN

    def update_interlocks(self, values: Interlock):
        if values.front_door == DoorSensor.OPEN:
            self.front_door.color = IndicatorColor.RED
        else:
            self.front_door.color = IndicatorColor.GREEN

        if values.rear_door == DoorSensor.OPEN:
            self.rear_door.color = IndicatorColor.RED
        else:
            self.rear_door.color = IndicatorColor.GREEN

        if values.limit_hoisting_bottom == LimitSwitch.ACTIVE:
            self.limit_hoisting_bottom.color = IndicatorColor.RED
        else:
            self.limit_hoisting_bottom.color = IndicatorColor.GREEN

        if values.limit_hoisting_top == LimitSwitch.ACTIVE:
            self.limit_hoisting_top.color = IndicatorColor.RED
        else:
            self.limit_hoisting_top.color = IndicatorColor.GREEN

        if values.limit_stabilizer_hoist_side == LimitSwitch.ACTIVE:
            self.limit_stablizer_hoist_side.color = IndicatorColor.RED
        else:
            self.limit_stablizer_hoist_side.color = IndicatorColor.GREEN

        if values.limit_stabilizer_opposite_hoist == LimitSwitch.ACTIVE:
            self.limit_stablizer_opposite_hoist.color = IndicatorColor.RED
        else:
            self.limit_stablizer_opposite_hoist.color = IndicatorColor.GREEN

    def CAN_reconnect(self):
        self.inputs.CAN_reconnect = True
        self.input_queue.put(copy.copy(self.inputs))
        self.inputs.CAN_reconnect = False

    def start_auto_button_action(self):
        self.inputs.run_auto = True
        self.input_queue.put(self.inputs)

    def stop_auto_button_action(self):
        self.inputs.run_auto = False
        self.input_queue.put(self.inputs)

    def add_initial_threads(self) -> None:
        worker = Worker(self.main_loop)
        worker.signals.progress.connect(self.update_ui)
        self.threadpool.start(worker)

    # Connects the input fields to a function that reads them into the inputs object
    def set_input_actions(self):
        self.start_auto_button.pressed.connect(self.start_auto_button_action)
        self.stop_auto_button.pressed.connect(self.stop_auto_button_action)
        self.refresh_log_list.pressed.connect(self.update_log_list)
        self.hoisting_enable.stateChanged.connect(self.get_inputs)
        self.hoisting_demand_value.valueChanged.connect(self.get_inputs)

        self.pump_open.stateChanged.connect(self.get_inputs)
        self.pump_enable.stateChanged.connect(self.get_inputs)
        self.pump_PID.valueChanged.connect(self.get_inputs)

        self.top_drive_rpm_set_point.valueChanged.connect(self.get_inputs)
        self.top_drive_torque_set_point.valueChanged.connect(self.get_inputs)
        self.top_drive_enable.stateChanged.connect(self.get_inputs)

        self.stop_button.clicked.connect(self.manual_stop)

    # All user inputs that is not a button uses this event so that not all events have their own function
    # The process is not data intensive so this is fine...
    def get_inputs(self):
        self.inputs.hoisting_enable = self.hoisting_enable.isChecked()
        self.inputs.hoisting_demand_value = self.hoisting_demand_value.value()

        self.inputs.pump_open = self.pump_open.isChecked()
        self.inputs.pump_enable = self.pump_enable.isChecked()
        self.inputs.pump_PID = self.pump_PID.value()

        self.inputs.top_drive_enable = self.top_drive_enable.isChecked()
        self.inputs.top_drive_rpm_set_point = self.top_drive_rpm_set_point.value()
        self.inputs.top_drive_torque_set_point = self.top_drive_torque_set_point.value()

        self.input_queue.put(self.inputs)

    # Sets all values to zero
    # If the plc has a non-zero state while the pc is at zero, this will not force send the value
    # This will need to be handled in a separate can message
    def manual_stop(self):
        self.hoisting_enable.setChecked(False)
        self.hoisting_demand_value.setValue(0.0)

        self.pump_open.setChecked(False)
        self.pump_enable.setChecked(False)
        self.pump_PID.setValue(0.0)

        self.top_drive_enable.setChecked(False)
        self.top_drive_rpm_set_point.setValue(0.0)
        self.top_drive_torque_set_point.setValue(0.0)

    def main_loop(self, progress_callback: pyqtSignal) -> str:
        display = 0
        while self.running:
            # The gui will sit here and wait until it receives new data from the main function
            display = self.display_queue.get()
            try:
                progress_callback.emit(display)
            except AttributeError:
                break
        return "Done"

    # Method used when starting the gui process
    @staticmethod
    def run_gui(display_queue, input_queue, GUI_management_queue, conf: dict):
        app = QApplication([])
        window = MainWindow(display_queue, input_queue, GUI_management_queue, conf)
        suppress_qt_warnings()
        app.exec_()
        # signals to the main process that the main window is closed
        GUI_management_queue.put(-1)
        window.running = False
