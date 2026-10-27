from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from .components import HeaderWidget, ContentWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RC BOLID CONTRO5L - Моніторинг і запуск")
        self.resize(1280, 720)
        self.setMinimumSize(1024, 576)

        self._init_ui()

    def _init_ui(self):
        central_widget = QWidget(self)
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header = HeaderWidget(central_widget)
        layout.addWidget(self.header, alignment=Qt.AlignmentFlag.AlignTop)

        self.content = ContentWidget(central_widget)
        layout.addWidget(self.content, 1)

    def on_telemetry_received(self, value: float):
        """Called when new telemetry data arrives."""
        if hasattr(self, 'content') and hasattr(self.content, 'speed'):
            self.content.speed.update_speed(value)

    @property
    def status_widget(self):
        return self.content.status

    @property
    def sensor_widget(self):
        return self.content.sensors