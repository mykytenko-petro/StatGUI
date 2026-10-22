from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox
)
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush


class BatteryWidget(QWidget):
    def __init__(self, parent: QWidget | None = None, level: int = 84):
        super().__init__(parent)
        self.level = level
        self.setFixedSize(36, 20)

    def set_level(self, level: int):
        self.level = max(0, min(100, level))
        self.update()

    def paintEvent(self, event): # type: ignore
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Battery outline
        painter.setPen(QPen(QColor("#94a3b8"), 1.2))
        painter.setBrush(QBrush(QColor("#031326")))
        painter.drawRoundedRect(1, 2, 28, 14, 3, 3)

        # Battery cap
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#94a3b8")))
        painter.drawRoundedRect(30, 6, 2, 6, 1, 1)

        # Battery fill bar
        fill_w = int(24 * (self.level / 100.0))
        if fill_w > 0:
            fill_color = QColor("#00e676") if self.level > 20 else QColor("#ef4444")
            painter.setBrush(QBrush(fill_color))
            painter.drawRoundedRect(3, 4, fill_w, 10, 2, 2)

        painter.end()


class HeaderWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName("HeaderWidget")
        self.setFixedHeight(50)

        self._init_ui()
        self._start_clock()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        title = QLabel("RC BOLID CONTROL", self)
        title.setObjectName("HeaderAppTitle")
        layout.addWidget(title)

        # Separator: |
        sep1 = QLabel("|", self)
        sep1.setObjectName("HeaderSeparator")
        layout.addWidget(sep1)

        # Subtitle: "Моніторинг і запуск"
        subtitle = QLabel("Моніторинг і запуск", self)
        subtitle.setObjectName("HeaderSubtitle")
        layout.addWidget(subtitle)

        # Bolid dropdown
        self.bolid_combo = QComboBox(self)
        self.bolid_combo.setObjectName("BolidSelector")
        self.bolid_combo.addItems(["BOLID-01  ∨", "BOLID-02  ∨", "BOLID-03  ∨"])
        layout.addWidget(self.bolid_combo)

        # Connected badge: ● Підключено
        self.status_badge = QFrame(self)
        self.status_badge.setObjectName("ConnectedBadge")
        badge_layout = QHBoxLayout(self.status_badge)
        badge_layout.setContentsMargins(10, 4, 12, 4)
        badge_layout.setSpacing(6)

        dot = QLabel("●", self.status_badge)
        dot.setObjectName("ConnectedBadgeDot")
        badge_layout.addWidget(dot)

        status_txt = QLabel("Підключено", self.status_badge)
        status_txt.setObjectName("ConnectedBadgeText")
        badge_layout.addWidget(status_txt)

        layout.addWidget(self.status_badge)

        layout.addStretch()

        # Battery
        self.battery_icon = BatteryWidget(self, 84)
        layout.addWidget(self.battery_icon)

        self.battery_label = QLabel("84%", self)
        self.battery_label.setObjectName("BatteryText")
        layout.addWidget(self.battery_label)

        sep2 = QLabel("|", self)
        sep2.setObjectName("HeaderSeparator")
        layout.addWidget(sep2)

        self.clock_label = QLabel(self)
        self.clock_label.setObjectName("ClockText")
        self._update_clock()
        layout.addWidget(self.clock_label)

        sep3 = QLabel("|", self)
        sep3.setObjectName("HeaderSeparator")
        layout.addWidget(sep3)

        self.settings_btn = QPushButton("⚙", self)
        self.settings_btn.setObjectName("HeaderIconButton")
        self.settings_btn.setToolTip("Налаштування")
        layout.addWidget(self.settings_btn)

        self.fullscreen_btn = QPushButton("⛶", self)
        self.fullscreen_btn.setObjectName("HeaderIconButton")
        self.fullscreen_btn.setToolTip("Повний екран")
        self.fullscreen_btn.clicked.connect(self._toggle_fullscreen)
        layout.addWidget(self.fullscreen_btn)

    def _start_clock(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_clock)
        self._timer.start(1000)

    def _update_clock(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.clock_label.setText(current_time)

    def _toggle_fullscreen(self):
        win = self.window()
        if win.isFullScreen(): # type: ignore
            win.showNormal() # type: ignore
        else:
            win.showFullScreen() # type: ignore
