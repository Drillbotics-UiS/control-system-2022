import logging
import math


class FlowController:
    def __init__(self, max_value=300, min_value=25):
        self._max = max_value
        self._min = min_value
        self._n = 0
        self._interval = math.ceil((max_value + min_value) / 2)

    def run(self) -> bool:
        if self._n >= self._interval - 1:
            logging.debug(f"GUI interval: {self._interval}")
            self._interval = int(self._interval * 0.95)
            if self._interval > self._max:
                self._interval = self._max
            elif self._interval < self._min:
                self._interval = self._min
            self._n = 0
            return True

        self._n += 1
        return False

    def slow_down(self):
        prev_interval = self._interval
        self._interval = int(self._interval * 1.05) + 10
        logging.info(f"GUI interval changed from {prev_interval} to {self._interval}")
