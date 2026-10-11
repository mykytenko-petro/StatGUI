from PyQt6.QtWidgets import QFrame, QWidget


class SensorsWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.setObjectName("SensorsWidget")
        self.setProperty("class", "card")
