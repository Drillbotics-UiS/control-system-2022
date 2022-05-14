class WeightOnBit:
    def __init__(self):
        self.sensor_1: float = 0.0
        self.sensor_2: float = 0.0
        self.sensor_3: float = 0.0
        self.sum: float = 0.0

    def __str__(self):
        return f"Sensor 1: {self.sensor_1}\tSensor 2: {self.sensor_2}\tSensor 3 {self.sensor_3}\tSUM: {self.sum}"
