import math
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)
from PyQt6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QFont
)


class SpeedometerDial(QWidget):
    def __init__(self, parent: QWidget | None = None, initial_speed: float = 42.0):
        super().__init__(parent)
        self.speed = initial_speed
        self.max_scale = 80.0
        self.setMinimumHeight(150)

    def set_speed(self, speed: float):
        self.speed = max(0.0, min(self.max_scale, speed))
        self.update()

    def paintEvent(self, event): # type: ignore
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        radius = min(w // 2 - 28, h - 35)
        cx = w / 2
        cy = h - 20

        arc_rect = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)

        # 1. Background Arc (track)
        track_pen = QPen(QColor("#152d4e"), 12)
        track_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(track_pen)
        painter.drawArc(arc_rect, 180 * 16, -180 * 16)

        # 2. Active Speed Arc
        fraction = min(1.0, max(0.0, self.speed / self.max_scale))
        if fraction > 0:
            active_pen = QPen(QColor("#ff5722"), 12)
            active_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(active_pen)
            span_angle = int(-180.0 * fraction * 16)
            painter.drawArc(arc_rect, 180 * 16, span_angle)

        # 3. Ticks and Labels (0, 20, 40, 60, 80)
        tick_values = [0, 20, 40, 60, 80]
        painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))

        for val in tick_values:
            frac = val / self.max_scale
            angle_rad = math.pi * (1.0 - frac)

            r_out = radius + 11
            r_in = radius + 4
            x1 = cx + r_in * math.cos(angle_rad)
            y1 = cy - r_in * math.sin(angle_rad)
            x2 = cx + r_out * math.cos(angle_rad)
            y2 = cy - r_out * math.sin(angle_rad)

            painter.setPen(QPen(QColor("#6482a6"), 1.5))
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            # Number text
            r_text = radius + 22
            tx = cx + r_text * math.cos(angle_rad)
            ty = cy - r_text * math.sin(angle_rad)
            
            painter.setPen(QPen(QColor("#8fa3c0")))
            text_rect = QRectF(tx - 14, ty - 8, 28, 16)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, str(val))

        # 4. Needle pointer (bold tapered indicator pointing to current value)
        needle_angle = math.pi * (1.0 - fraction)
        r_needle_start = radius * 0.60
        r_needle_end = radius + 2
        nx1 = cx + r_needle_start * math.cos(needle_angle)
        ny1 = cy - r_needle_start * math.sin(needle_angle)
        nx2 = cx + r_needle_end * math.cos(needle_angle)
        ny2 = cy - r_needle_end * math.sin(needle_angle)

        needle_pen = QPen(QColor("#ff5722"), 4)
        needle_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(needle_pen)
        painter.drawLine(QPointF(nx1, ny1), QPointF(nx2, ny2))

        # 5. Center Big Speed Value
        painter.setPen(QPen(QColor("#ffffff")))
        painter.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        speed_rect = QRectF(cx - 50, cy - 68, 100, 46)
        painter.drawText(speed_rect, Qt.AlignmentFlag.AlignCenter, f"{int(round(self.speed))}")

        # Unit underneath
        painter.setPen(QPen(QColor("#8fa3c0")))
        painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        unit_rect = QRectF(cx - 50, cy - 20, 100, 18)
        painter.drawText(unit_rect, Qt.AlignmentFlag.AlignCenter, "км/год")

        painter.end()


class SpeedWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setObjectName("SpeedWidget")
        self.setProperty("class", "card")

        self.max_speed = 57.0
        self.current_speed = 1.0

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        # Header
        title = QLabel("Швидкість", self)
        title.setObjectName("SpeedTitle")
        layout.addWidget(title)

        # Speedometer Dial
        self.dial = SpeedometerDial(self, self.current_speed)
        layout.addWidget(self.dial, 1)

        # Bottom sub-card with Max Speed and Status
        sub_card = QFrame(self)
        sub_card.setObjectName("SpeedSubCard")
        sub_layout = QHBoxLayout(sub_card)
        sub_layout.setContentsMargins(12, 8, 12, 8)
        sub_layout.setSpacing(10)

        # Left: Max speed
        max_col = QVBoxLayout()
        max_col.setSpacing(2)
        max_col.setContentsMargins(0, 0, 0, 0)

        max_label = QLabel("Максимальна", sub_card)
        max_label.setObjectName("SpeedSubLabel")

        max_val_layout = QHBoxLayout()
        max_val_layout.setSpacing(4)
        self.max_val_num = QLabel(f"{int(self.max_speed)}", sub_card)
        self.max_val_num.setObjectName("SpeedMaxVal")
        self.max_val_unit = QLabel("км/год", sub_card)
        self.max_val_unit.setObjectName("SpeedMaxUnit")
        max_val_layout.addWidget(self.max_val_num)
        max_val_layout.addWidget(self.max_val_unit)
        max_val_layout.addStretch()

        max_col.addWidget(max_label)
        max_col.addLayout(max_val_layout)
        sub_layout.addLayout(max_col, 1)

        # Divider
        divider = QLabel("|", sub_card)
        divider.setObjectName("SpeedSubDivider")
        sub_layout.addWidget(divider)

        # Right: Status
        status_col = QVBoxLayout()
        status_col.setSpacing(2)
        status_col.setContentsMargins(0, 0, 0, 0)

        status_lbl = QLabel("Статус:", sub_card)
        status_lbl.setObjectName("SpeedSubLabel")

        status_val_layout = QHBoxLayout()
        status_val_layout.setSpacing(6)
        self.status_dot = QLabel("●", sub_card)
        self.status_dot.setObjectName("SpeedStatusDot")
        self.status_text = QLabel("Рух", sub_card)
        self.status_text.setObjectName("SpeedStatusText")
        status_val_layout.addWidget(self.status_dot)
        status_val_layout.addWidget(self.status_text)
        status_val_layout.addStretch()

        status_col.addWidget(status_lbl)
        status_col.addLayout(status_val_layout)
        sub_layout.addLayout(status_col, 1)

        layout.addWidget(sub_card)

    def update_speed(self, speed: float):
        self.current_speed = speed
        if speed > self.max_speed:
            self.max_speed = speed
            self.max_val_num.setText(f"{int(self.max_speed)}")

        self.dial.set_speed(speed)

        if speed > 0:
            self.status_text.setText("Рух")
            self.status_dot.setStyleSheet("color: #00e676;")
            self.status_text.setStyleSheet("color: #00e676; font-weight: bold; font-size: 15px;")
        else:
            self.status_text.setText("Стоїть")
            self.status_dot.setStyleSheet("color: #64748b;")
            self.status_text.setStyleSheet("color: #94a3b8; font-weight: bold; font-size: 15px;")
