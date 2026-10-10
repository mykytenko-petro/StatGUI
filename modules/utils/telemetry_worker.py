import socket

from PyQt6.QtCore import QThread, pyqtSignal


class TelemetryWorker(QThread):
    data_received = pyqtSignal(float)

    def __init__(self, host='127.0.0.1', port=5005):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = None
        self.running = True

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.5)
        self.sock.bind((self.host, self.port))

        while self.running:
            try:
                data, _ = self.sock.recvfrom(1024)
                val = float(data.decode('utf-8').strip())
                self.data_received.emit(val)
            except socket.timeout:
                continue
            except ValueError:
                continue
            except OSError:
                break

        self.sock.close()

    def stop(self):
        self.running = False
        self.wait()