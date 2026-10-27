from ..views.components.sensors import SensorsWidget

from ..services import ServerWorker


class TelemetryController:
    def __init__(
            self,
            server_worker: ServerWorker,
            sensors_widget: SensorsWidget
        ) -> None:
        self._sensors_widget = sensors_widget
        
        server_worker.data_received.connect(self._on_data_recieved)
        
    def _on_data_recieved(self, data: dict):
        self._sensors_widget.update_sensors([
            data["LEFT"],
            data["MIDDLE"],
            data["RIGHT"],
            data["FAR_LEFT"],
            data["FAR_RIGHT"],
        ])