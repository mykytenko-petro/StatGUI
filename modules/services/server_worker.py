import json
import socket
from PyQt6.QtCore import QThread, pyqtSignal


class ServerWorker(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, host='0.0.0.0', port=5005, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self.sock = None
        self._peer_address = None
        self.running = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)
        sock.bind((self.host, self.port))
        
        self.sock = sock

        try:
            while self.running:
                try:
                    data, peer_address = sock.recvfrom(1024)
                    self._peer_address = peer_address

                    self.data_received.emit(json.loads(data.decode()))
                except socket.timeout:
                    continue
                except ValueError:
                    continue
                except OSError:
                    # Occurs when socket is closed externally in stop()
                    break
        finally:
            self.sock = None
            self._peer_address = None
            sock.close()

    def send_data(self, data: dict) -> int:
        sock = self.sock
        peer_address = self._peer_address

        if sock is None:
            raise RuntimeError("Telemetry worker is not running")
        if peer_address is None:
            raise RuntimeError("No UDP device has sent data yet")

        payload = json.dumps(data).encode()
        return sock.sendto(payload, peer_address)

    def stop(self):
        self.running = False
        sock = self.sock
        if sock:
            try:
                sock.close()
            except OSError:
                pass
        self.wait()