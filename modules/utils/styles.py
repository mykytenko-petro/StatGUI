from PyQt6.QtWidgets import QApplication


def set_styles(app: QApplication):
    with open("assets/styles/style.qss", "r") as main_style:
        styles = main_style.read()
        
        app.setStyleSheet(styles)
