from PyQt6.QtWidgets import QFrame, QWidget


class HeaderWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.setObjectName("HeaderWidget")
