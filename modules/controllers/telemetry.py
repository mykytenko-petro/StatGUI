from ..views.components.speed import SpeedWidget
from ..views.components.sensors import SensorsWidget
from ..services import ServerWorker


class TelemetryController:
    def __init__(
            self,
            server_worker: ServerWorker,
            sensors_widget: SensorsWidget,
            speed_widget: SpeedWidget
        ) -> None:
        self._sensors_widget = sensors_widget
        self._speed_widget = speed_widget
        
        server_worker.data_received.connect(self._on_data_recieved)
        
    def _on_data_recieved(self, data: dict):
        self._sensors_widget.update_sensors([
            data.get("LEFT"),
            data.get("MIDDLE"),
            data.get("RIGHT"),
            data.get("FAR_LEFT"),
            data.get("FAR_RIGHT"),
        ])

        self._speed_widget.update_speed(data["RPM"])
