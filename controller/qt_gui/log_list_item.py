from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout

from logger.log_file_manager import LogFileManager


class LogListItem(QHBoxLayout):
    def __init__(self, log_file_manager: LogFileManager, filename: str):
        super().__init__()
        self._filename = filename
        self._log_file_manager = log_file_manager
        font = QFont()
        font.setPointSize(12)

        self._filename_label = QLabel(text=self._filename)
        self._filename_label.setFont(font)
        self.addWidget(self._filename_label)
        self._export_button = QPushButton(text="Export")
        self._export_button.setFont(font)
        self._export_button.pressed.connect(self.export_button_action)
        self.addWidget(self._export_button)
        self._delete_button = QPushButton(text="Delete")
        self._delete_button.setFont(font)
        self._delete_button.pressed.connect(self.delete_button_action)
        self.addWidget(self._delete_button)

    # Removes the buttons and labels when the layout is deleted.
    def __del__(self):
        self._delete_button.close()
        self._export_button.close()
        self._filename_label.close()

    def delete_button_action(self):
        self._log_file_manager.delete_file(self._filename)
        self.deleteLater()

    def export_button_action(self):
        self._log_file_manager.export_file(self._filename)
