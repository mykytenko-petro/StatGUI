from PyQt6.QtWidgets import QWidget, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stats")
        self.resize(1280, 720)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
                
        self.setLayout(layout)