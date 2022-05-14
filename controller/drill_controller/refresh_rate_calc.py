import time


class RefreshRateCalc:
    def __init__(self, interval=100):
        self._update_interval = interval
        self._data_count = 0
        self._last_time_reading = time.time()
        self._frequency = 0

    def update(self) -> float:
        self._data_count += 1
        if self._data_count >= self._update_interval:
            time_now = time.time()
            self._frequency = float(self._data_count) / (time_now - self._last_time_reading)
            self._last_time_reading = time_now
            self._data_count = 0
        return self._frequency
