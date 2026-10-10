import sys

from PyQt6.QtWidgets import QApplication

from modules import (
    set_styles,
    TelemetryWorker,
    MainWindow
)


def main():
    app = QApplication(sys.argv)

    set_styles(app)

    telemetry_worker = TelemetryWorker()
    app.aboutToQuit.connect(telemetry_worker.stop)
    telemetry_worker.start()

    window = MainWindow()
    window.show()
    
    app.exec()

if __name__ == "__main__":
    main()