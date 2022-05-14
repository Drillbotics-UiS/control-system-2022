from PyQt5.QtCore import QObject, pyqtSignal

from data_models.display_data import DisplayData


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(DisplayData)
