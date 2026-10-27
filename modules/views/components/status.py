from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import QTimer, pyqtSignal, Qt


class StatusWidget(QFrame):
    started = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setObjectName("StatusWidget")
        self.setProperty("class", "card")

        self._elapsed_seconds = 3
        self._is_running = False

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._on_tick)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Стартова послідовність", self)
        title.setObjectName("StatusTitle")
        header_row.addWidget(title)

        header_row.addStretch()

        self.ready_badge = QFrame(self)
        self.ready_badge.setObjectName("ReadyBadge")
        ready_layout = QHBoxLayout(self.ready_badge)
        ready_layout.setContentsMargins(8, 2, 8, 2)
        ready_layout.setSpacing(5)

        dot = QLabel("●", self.ready_badge)
        dot.setObjectName("ReadyBadgeDot")
        ready_layout.addWidget(dot)

        self.ready_text = QLabel("ГОТОВИЙ ДО СТАРТУ", self.ready_badge)
        self.ready_text.setObjectName("ReadyBadgeText")
        ready_layout.addWidget(self.ready_text)

        header_row.addWidget(self.ready_badge)
        layout.addLayout(header_row)

        mid_layout = QHBoxLayout()
        mid_layout.setContentsMargins(0, 4, 0, 4)
        mid_layout.setSpacing(8)

        checklist_layout = QVBoxLayout()
        checklist_layout.setSpacing(6)
        checklist_layout.setContentsMargins(0, 0, 0, 0)

        items = [
            "Зв'язок стабільний",
            "Датчики готові",
            "Траса вільна"
        ]
        for text in items:
            row = QHBoxLayout()
            row.setSpacing(8)
            check_icon = QLabel("✔", self)
            check_icon.setObjectName("CheckmarkIcon")
            check_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

            label = QLabel(text, self)
            label.setObjectName("CheckmarkLabel")

            row.addWidget(check_icon)
            row.addWidget(label)
            row.addStretch()
            checklist_layout.addLayout(row)

        mid_layout.addLayout(checklist_layout, 1)

        # Big Timer
        self.timer_label = QLabel("00:00", self)
        self.timer_label.setObjectName("TimerLabel")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        mid_layout.addWidget(self.timer_label)

        layout.addLayout(mid_layout)

        # Buttons
        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(0, 2, 0, 2)
        buttons_layout.setSpacing(8)

        self.start_btn = QPushButton("▶   ЗАПУСТИТИ БОЛІД", self)
        self.start_btn.setObjectName("StartButton")
        self.start_btn.clicked.connect(self.start)

        self.stop_btn = QPushButton("■   АВАРІЙНА ЗУПИНКА", self)
        self.stop_btn.setObjectName("StopButton")
        self.stop_btn.clicked.connect(self.stop)

        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.stop_btn)

        layout.addLayout(buttons_layout)

    def start(self):
        if not self._is_running:
            self._is_running = True
            self._elapsed_seconds = 0
            self.timer_label.setText("00:00")
            self._timer.start()
            self.ready_text.setText("У РУСІ")
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.started.emit()

    def stop(self):
        if self._is_running:
            self._is_running = False
            self._timer.stop()
        self.ready_text.setText("ЗУПИНЕНО")
        self.start_btn.setEnabled(True)
        self.stopped.emit()

    def _on_tick(self):
        self._elapsed_seconds += 1
        minutes = self._elapsed_seconds // 60
        seconds = self._elapsed_seconds % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
