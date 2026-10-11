from PyQt6.QtWidgets import QFrame, QWidget


class EventsWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.setObjectName("EventsWidget")
        self.setProperty("class", "card")
