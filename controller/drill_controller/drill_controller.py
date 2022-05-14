from numpy.random import uniform

from data_models.base_control_data import BaseControlData
from data_models.dh_sensor_data import DHSensorData
from data_models.display_data import DisplayData
from data_models.manual_control_data import ManualControlData
from data_models.path_models import MinimumCurvaturePath
from data_models.plc_sensor_data import PLCSensorData
from data_models.user_input import UserInput
from drill_controller.refresh_rate_calc import RefreshRateCalc
from drill_controller.timer import Timer


class DrillController:
    def __init__(self):
        self._control_mode = 0
        self._timer = Timer()
        self._manual_control_data = ManualControlData()
        self._automatic_control_data = BaseControlData()
        self._plc_sensor_data = PLCSensorData()
        self._dhs_data = DHSensorData()
        self._user_input = UserInput()
        self._display_data = DisplayData()
        self.PLC_refresh_rate_calc = RefreshRateCalc()
        self.GUI_refresh_rate_calc = RefreshRateCalc(30)
        self.DHS_refresh_rate_calc = RefreshRateCalc(10)
        self._target_point = (uniform(-30, 30), uniform(-30, 30), -uniform(50, 60))
        self._minimum_curvature_path = MinimumCurvaturePath((0, 0, 0), self._target_point)
        self._well_log_depth = 0

    @property
    def control_mode(self):
        return self._control_mode

    def plc_sensor_input(self, sensor_data: PLCSensorData):
        self._display_data.refresh_rate.PLC = self.PLC_refresh_rate_calc.update()
        self._plc_sensor_data = sensor_data
        self._display_data.temp_circulation_system = sensor_data.temp_circulation_system
        self._display_data.pressure_circulation_system = sensor_data.pressure_circulation_system
        self._display_data.hoisting_height = sensor_data.hoisting_height
        self._display_data.interlock = sensor_data.interlock
        self._display_data.wob = sensor_data.wob

    def dh_sensor_input(self, sensor_data: DHSensorData):
        self._display_data.refresh_rate.DHS = self.DHS_refresh_rate_calc.update()
        self._dhs_data = sensor_data

    def receive_user_input(self, user_input: UserInput):
        self._user_input = user_input
        self._control_mode = user_input.control_mode
        self._timer.running = user_input.run_auto

    def generate_control_output(self):
        self._manual_control_data.force_send = self._user_input.force_send
        self._manual_control_data.control_mode = self._user_input.control_mode

        self._manual_control_data.hoisting_demand_value = self._user_input.hoisting_demand_value
        self._manual_control_data.hoisting_enable = int(self._user_input.hoisting_enable)

        self._manual_control_data.pump_enable = int(self._user_input.pump_enable)
        self._manual_control_data.pump_open = int(self._user_input.pump_open)
        self._manual_control_data.pump_PID = self._user_input.pump_PID

        self._manual_control_data.top_drive_enable = int(self._user_input.top_drive_enable)
        self._manual_control_data.top_drive_rpm_set_point = self._user_input.top_drive_rpm_set_point
        self._manual_control_data.top_drive_torque_set_point = self._user_input.top_drive_torque_set_point
        return self

    # Output to the plc
    def get_can_output(self):
        match self._control_mode:
            case 0:
                return self._manual_control_data.to_can()

    # Estimated bit position etc...
    def gui_output(self):
        self._display_data.refresh_rate.GUI = self.GUI_refresh_rate_calc.update()
        # print(f"PLC: {self._display_data.refresh_rate.PLC} GUI: {self._display_data.refresh_rate.GUI} DHS: {self._display_data.refresh_rate.DHS}")
        self._display_data.DHS_CAN_timed_out = self._dhs_data.timed_out
        self._display_data.PLC_CAN_timed_out = self._plc_sensor_data.timed_out
        self._display_data.estimated_position = self._minimum_curvature_path.get_next_point()
        self._display_data.well_log_data.populate_randomly(self._well_log_depth)
        self._display_data.tension_log_data.populate_randomly(self._well_log_depth)
        self._display_data.target_point = self._target_point
        self._display_data.elapsed_time = self._timer.elapsed_time
        self._well_log_depth += 1
        self._well_log_depth %= 1000
        return self._display_data
