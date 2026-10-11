from PyQt6.QtWidgets import QFrame, QWidget


class CameraWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.setObjectName("CameraWidget")
        self.setProperty("class", "card")
