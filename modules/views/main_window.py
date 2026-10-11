from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from .components import HeaderWidget, ContentWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stats")
        self.resize(1280, 720)

        self._init_ui()

    def _init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        header = HeaderWidget(central_widget)
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignTop)

        content = ContentWidget(central_widget)

        layout.addWidget(content, 1)
