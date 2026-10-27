from ..services import ServerWorker
from ..views.components.status import StatusWidget


class CommandController:
    def __init__(
            self,
            server_worker: ServerWorker,
            status_widget: StatusWidget
        ) -> None:
        self._server_worker = server_worker
        
        status_widget.started.connect(self._on_started)
        status_widget.stopped.connect(self._on_stopped)

    def _on_started(self):
        try:
            self._server_worker.send_data({"cmd": "test:led_on"})
        except RuntimeError as e:
            print(f"[CommandController] Failed to send start command: {e}")

    def _on_stopped(self):
        try:
            self._server_worker.send_data({"cmd": "test:led_off"})
        except RuntimeError as e:
            print(f"[CommandController] Failed to send stop command: {e}")


