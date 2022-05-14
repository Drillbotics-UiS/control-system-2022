from PyQt5.QtWidgets import QLabel

from data_models.enums import IndicatorColor


class IndicatorLED(QLabel):
    def __init__(self):
        super().__init__()
        self._color = IndicatorColor.RED
        self._size = 40
        self.__generate_css()

    @property
    def border_radius(self):
        return self._size // 2

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if self._size != value:
            self._size = value
            self.__generate_css()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if self._color != value:
            self._color = value
            self.__generate_css()

    def __generate_css(self):
        self.setStyleSheet(
            f"max-width: {self.size}px;\n"
            f"max-height: {self.size}px;\n"
            f"min-width: {self.size}px;\n"
            f"min-height: {self.size}px;\n"
            f"border-radius: {self.border_radius}px;\n"
            f"border-style: solid;\n"
            f"border-color: black;\n"
            f"border-width: 2px;\n"
            f"background-color: {self._color.value}\n"
        )
