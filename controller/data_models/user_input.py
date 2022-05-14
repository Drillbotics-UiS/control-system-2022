import time


# Data that is returned from the gui
class UserInput:
    def __init__(self):
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.force_send = False

        self.run_auto = False

        self.CAN_reconnect = False

        self.control_mode = 0
        self.hoisting_enable = False
        self.hoisting_demand_value = 0.0

        self.pump_enable = False
        self.pump_PID = 0.0
        self.pump_open = False

        self.top_drive_enable = False
        self.top_drive_rpm_set_point = 0.0
        self.top_drive_torque_set_point = 0.0

    def write_to_db(self, conn):
        fields = ('force_send', 'CAN_reconnect', 'control_mode', 'hoisting_enable', 'hoisting_demand_value',
                  'pump_enable', 'pump_PID', 'pump_open', 'top_drive_enable', 'top_drive_rpm_set_point',
                  'top_drive_torque_set_point', 'timestamp')
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        for f in fields:
            assert hasattr(self, f)
        conn.execute(
            f"INSERT INTO user_input({','.join(fields)}) VALUES ({','.join('?' * len(fields))})",
            tuple(getattr(self, f) for f in fields)
        )
