from pathlib import Path
from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QPixmap


class CameraFeedDisplay(QLabel):
    """Displays the camera view placeholder."""
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("CameraFeedDisplay")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._feed_pixmap = None
        feed_path = Path("assets/images/camera_feed.jpg")
        if feed_path.exists():
            self._feed_pixmap = QPixmap(str(feed_path))

    def resizeEvent(self, event): # type: ignore
        super().resizeEvent(event)
        self._update_display()

    def _update_display(self):
        if self._feed_pixmap and not self._feed_pixmap.isNull():
            scaled = self._feed_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            x = max(0, (scaled.width() - self.width()) // 2)
            y = max(0, (scaled.height() - self.height()) // 2)
            cropped = scaled.copy(x, y, self.width(), self.height())
            self.setPixmap(cropped)


class CameraWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setObjectName("CameraWidget")
        self.setProperty("class", "card")

        self._init_ui()
        self._start_clock()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 12)
        layout.setSpacing(8)

        # Header Row: "Камера боліда" + "● LIVE" badge
        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Камера боліда", self)
        title.setObjectName("CameraTitle")
        header_row.addWidget(title)

        live_badge = QFrame(self)
        live_badge.setObjectName("CameraLiveBadge")
        badge_layout = QHBoxLayout(live_badge)
        badge_layout.setContentsMargins(8, 2, 8, 2)
        badge_layout.setSpacing(5)

        dot = QLabel("●", live_badge)
        dot.setObjectName("LiveBadgeDot")
        badge_layout.addWidget(dot)

        txt = QLabel("LIVE", live_badge)
        txt.setObjectName("LiveBadgeText")
        badge_layout.addWidget(txt)

        header_row.addWidget(live_badge)
        header_row.addStretch()

        layout.addLayout(header_row)

        # Video feed container
        self.feed_container = QFrame(self)
        self.feed_container.setObjectName("CameraFeedContainer")
        feed_layout = QVBoxLayout(self.feed_container)
        feed_layout.setContentsMargins(0, 0, 0, 0)

        self.feed_display = CameraFeedDisplay(self.feed_container)
        feed_layout.addWidget(self.feed_display)

        # Dynamic overlay at bottom-right for live timestamp: ● LIVE • 17:14:48
        self.time_badge = QLabel(self.feed_container)
        self.time_badge.setObjectName("CameraOverlayBadgeLive")
        self._update_time_badge()

        layout.addWidget(self.feed_container, 1)

    def resizeEvent(self, event): # type: ignore
        super().resizeEvent(event)
        fc_w = self.feed_container.width()
        fc_h = self.feed_container.height()
        tb_w = self.time_badge.sizeHint().width()
        tb_h = self.time_badge.sizeHint().height()
        self.time_badge.move(fc_w - tb_w - 12, fc_h - tb_h - 12)

    def _start_clock(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_time_badge)
        self._timer.start(1000)

    def _update_time_badge(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_badge.setText(f"● LIVE • {current_time}")
        self.time_badge.adjustSize()
        fc_w = self.feed_container.width()
        fc_h = self.feed_container.height()
        tb_w = self.time_badge.width()
        tb_h = self.time_badge.height()
        self.time_badge.move(fc_w - tb_w - 12, fc_h - tb_h - 12)
