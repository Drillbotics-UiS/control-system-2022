import time


class Timer:
    def __init__(self):
        self._start_time = time.time()

        self._running: bool = False

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        if value and not self._running:
            self._start_time = time.time()
        self._running = value

    @property
    def elapsed_time(self) -> float:
        if self._running:
            return time.time() - self._start_time
        return 0.0
