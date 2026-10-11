from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QHBoxLayout,
    QVBoxLayout
)

from .camera import CameraWidget
from .status import StatusWidget
from .sensors import SensorsWidget


class ContentWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setObjectName("ContentWidget")

        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        left_container = QFrame()
        left_container.setObjectName("LeftContainer")
        left_container_layout = QVBoxLayout(left_container)
        layout.addWidget(left_container)

        bottom_left_container = QFrame()
        bottom_left_container.setObjectName("BottomLeftContainer")
        bottom_left_container_layout = QHBoxLayout(bottom_left_container)
        bottom_left_container_layout.setContentsMargins(0, 0, 0, 0)

        right_container = QFrame()
        right_container.setObjectName("RightContainer")
        right_container_layout = QVBoxLayout(right_container) # TODO: use this layout
        layout.addWidget(right_container, 1)
        
        camera = CameraWidget(self)
        left_container_layout.addWidget(camera)

        left_container_layout.addWidget(bottom_left_container, 1)

        status = StatusWidget(bottom_left_container)
        sensors = SensorsWidget(bottom_left_container)

        bottom_left_container_layout.addWidget(status)
        bottom_left_container_layout.addWidget(sensors)



