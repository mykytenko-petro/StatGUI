from PyQt6.QtWidgets import QFrame, QWidget


class SpeedWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.setObjectName("SpeedWidget")
        self.setProperty("class", "card")
