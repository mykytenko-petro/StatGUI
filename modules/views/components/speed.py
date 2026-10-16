from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class SpeedWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.setObjectName("SpeedWidget")
        self.setProperty("class", "card")

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        self.speed_label = QLabel(self)
        self.speed_label.setObjectName("SpeedLabel")
        self.speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.update_speed(2232)

        layout.addWidget(self.speed_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def update_speed(self, speed: float):
        self.speed_label.setText(str(speed) + "\nkm/hr")
