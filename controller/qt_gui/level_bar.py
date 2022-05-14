from PyQt5 import QtCore
from PyQt5.QtWidgets import QProgressBar, QSizePolicy


class LevelBar(QProgressBar):
    def __init__(self, max_value: int, warning_value, critical_value):
        super().__init__()
        self._critical_value = critical_value
        self._warning_values: range = range(warning_value, critical_value)
        self._safe_values: range = range(0, warning_value)
        self._previous_value = -1
        self.setOrientation(QtCore.Qt.Vertical)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMaximum(max_value)
        self.setTextVisible(False)

    def setValue(self, value: int) -> None:
        if value > self.maximum():
            value = self.maximum()
        super().setValue(value)
        if value >= self._critical_value > self._previous_value:
            style = "QProgressBar::chunk {background-color: qlineargradient(x1:0, y1:0.5,x2:1,y2:0.5,stop:0 #ff0000, " \
                    "stop:1 #aa0000);} "
            self.__update_css(style)
        elif (value in self._warning_values) and (self._previous_value not in self._warning_values):
            style = "QProgressBar::chunk {background-color: qlineargradient(x1:0, y1:0.5,x2:1,y2:0.5,stop:0 #ffff00, " \
                    "stop:1 #aaaa00);} "
            self.__update_css(style)
        elif value in self._safe_values and self._previous_value not in self._safe_values:
            style = "QProgressBar::chunk {background-color: qlineargradient(x1:0, y1:0.5,x2:1,y2:0.5,stop:0 #00ff00, " \
                    "stop:1 #00aa00);} "
            self.__update_css(style)
        self._previous_value = value

    def __update_css(self, css: str):
        self.setStyleSheet(css)
