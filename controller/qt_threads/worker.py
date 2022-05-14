import sys
import traceback

from PyQt5.QtCore import QRunnable, pyqtSlot

from qt_threads.worker_signals import WorkerSignals


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self) -> None:
        # runtime exceptions are for when the gui is removed from the main function
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            try:
                traceback.print_exc()
                exc_type, value = sys.exc_info()[:2]
                self.signals.error.emit((exc_type, value, traceback.format_exc()))
            except RuntimeError:
                pass
        else:
            try:
                self.signals.result.emit(result)
            except RuntimeError:
                pass
        finally:
            try:
                self.signals.finished.emit()
            except RuntimeError:
                pass
