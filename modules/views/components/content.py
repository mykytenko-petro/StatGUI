from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QHBoxLayout,
    QVBoxLayout
)

from .camera import CameraWidget
from .status import StatusWidget
from .sensors import SensorsWidget
from .speed import SpeedWidget
from .events import EventsWidget


class ContentWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName("ContentWidget")

        self._init_ui()

    def _init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Left Column (Camera + Bottom row)
        left_container = QFrame(self)
        left_container.setObjectName("LeftContainer")
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        # 1. Camera Widget
        self.camera = CameraWidget(left_container)
        left_layout.addWidget(self.camera, 60)

        # 2. Bottom Row (Status + Sensors)
        bottom_left_container = QFrame(left_container)
        bottom_left_container.setObjectName("BottomLeftContainer")
        bottom_layout = QHBoxLayout(bottom_left_container)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(10)

        self.status = StatusWidget(bottom_left_container)
        self.sensors = SensorsWidget(bottom_left_container)

        bottom_layout.addWidget(self.status, 44)
        bottom_layout.addWidget(self.sensors, 56)

        left_layout.addWidget(bottom_left_container, 40)

        main_layout.addWidget(left_container, 72)

        # Right Column (Speed + Events)
        right_container = QFrame(self)
        right_container.setObjectName("RightContainer")
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        self.speed = SpeedWidget(right_container)
        self.events = EventsWidget(right_container)

        right_layout.addWidget(self.speed, 48)
        right_layout.addWidget(self.events, 52)

        main_layout.addWidget(right_container, 28)
