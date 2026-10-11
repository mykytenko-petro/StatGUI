from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton
)
from PyQt6.QtCore import QTimer, pyqtSignal


class StatusWidget(QFrame):
    started = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.setObjectName("StatusWidget")
        self.setProperty("class", "card")

        self._elapsed_seconds = 0
        self._is_running = False

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._on_tick)

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        title = QLabel("Status", self)
        title.setObjectName("StatusTitle")
        layout.addWidget(title)

        self.status_label = QLabel("STOPPED", self)
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setProperty("status", "stopped")
        layout.addWidget(self.status_label)

        self.timer_label = QLabel("00:00", self)
        self.timer_label.setObjectName("TimerLabel")
        layout.addWidget(self.timer_label)

        layout.addStretch()

        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(8)

        self.start_btn = QPushButton("Start", self)
        self.start_btn.setObjectName("StartButton")
        self.start_btn.clicked.connect(self.start)

        self.stop_btn = QPushButton("Stop", self)
        self.stop_btn.setObjectName("StopButton")
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)

        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.stop_btn)

        layout.addLayout(buttons_layout)

    def _connect_signals(self):
        self.started.connect(lambda: print("Start"))
        self.stopped.connect(lambda: print("Stop"))

    def start(self):
        if not self._is_running:
            self._is_running = True
            self._elapsed_seconds = 0
            self.timer_label.setText("00:00")
            self._timer.start()
            self.status_label.setText("RUNNING")
            self.status_label.setProperty("status", "running")
            self.status_label.style().unpolish(self.status_label) # type: ignore
            self.status_label.style().polish(self.status_label) # type: ignore
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.started.emit()

    def stop(self):
        if self._is_running:
            self._is_running = False
            self._timer.stop()
            self.status_label.setText("STOPPED")
            self.status_label.setProperty("status", "stopped")
            self.status_label.style().unpolish(self.status_label) # type: ignore
            self.status_label.style().polish(self.status_label) # type: ignore
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.stopped.emit()

    def _on_tick(self):
        self._elapsed_seconds += 1
        minutes = self._elapsed_seconds // 60
        seconds = self._elapsed_seconds % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
