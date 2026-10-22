import json
import socket
from threading import Lock
from PyQt6.QtCore import QThread, pyqtSignal


class TelemetryWorker(QThread):
    data_received = pyqtSignal(float)

    def __init__(self, host='0.0.0.0', port=5005, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self.sock = None
        self._peer_address = None
        self._socket_lock = Lock()
        self.running = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)
        sock.bind((self.host, self.port))
        
        with self._socket_lock:
            self.sock = sock

        try:
            while self.running:
                try:
                    data, peer_address = sock.recvfrom(1024)
                    with self._socket_lock:
                        self._peer_address = peer_address

                    print(data)
                    val = float(data.decode().strip())
                    self.data_received.emit(val)
                except socket.timeout:
                    continue
                except ValueError:
                    # Ignore invalid incoming payload formats
                    continue
                except OSError:
                    # Socket closed or unrecoverable error
                    break
        finally:
            with self._socket_lock:
                self.sock = None
                self._peer_address = None
            sock.close()

    def send_data(self, data: dict) -> int:
        payload = json.dumps(data).encode()

        with self._socket_lock:
            if self.sock is None:
                raise RuntimeError("Telemetry worker is not running")
            if self._peer_address is None:
                raise RuntimeError("No UDP device has sent data yet")
            
            # Send while holding lock or using snapshotted references
            return self.sock.sendto(payload, self._peer_address)

    def stop(self):
        self.running = False
        with self._socket_lock:
            if self.sock:
                try:
                    self.sock.close()
                except OSError:
                    pass
        self.wait()  # Wait for QThread to finish cleanly