import sys

from PyQt6.QtWidgets import QApplication

from modules import (
    set_styles,
    ServerWorker,
    MainWindow,
    CommandController,
    TelemetryController
)


def main():
    app = QApplication(sys.argv)

    set_styles(app)

    window = MainWindow()

    server_worker = ServerWorker()
    server_worker.data_received.connect(window.on_telemetry_received)
    app.aboutToQuit.connect(server_worker.stop)
    server_worker.start()

    CommandController(server_worker, window.status_widget)
    TelemetryController(server_worker, window.sensor_widget)

    window.show()

    app.exec()

if __name__ == "__main__":
    main()