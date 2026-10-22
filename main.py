import sys

from PyQt6.QtWidgets import QApplication

from modules import (
    set_styles,
    TelemetryWorker,
    MainWindow,
    CommandController,
)


def main():
    app = QApplication(sys.argv)

    set_styles(app)

    window = MainWindow()

    telemetry_worker = TelemetryWorker()
    telemetry_worker.data_received.connect(window.on_telemetry_received)
    app.aboutToQuit.connect(telemetry_worker.stop)
    telemetry_worker.start()

    command_controller = CommandController(
        telemetry_worker=telemetry_worker,
        status_widget=window.status_widget,
    )
    window.command_controller = command_controller # type: ignore

    window.show()

    app.exec()



if __name__ == "__main__":
    main()