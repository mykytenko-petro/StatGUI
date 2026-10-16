from PyQt6.QtWidgets import QFrame, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class EventsWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.setObjectName("EventsWidget")
        self.setProperty("class", "card")

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(20, 5, 0, 20)

        name_label = QLabel("Події")
        layout.addWidget(name_label)
        
        event_card_container = QFrame()
        layout.addWidget(event_card_container)

        
