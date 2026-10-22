from pathlib import Path
from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap


class SensorBox(QFrame):
    """Individual card for one distance sensor."""
    def __init__(self, sensor_id: str, name: str, value: float, parent: QWidget | None = None):
        super().__init__(parent)
        self.sensor_id = sensor_id
        self.sensor_name = name
        self.value = value
        self.setObjectName("SensorBox")

        self._init_ui()
        self.set_value(value)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(1)

        # Top line: "S1  Передній лівий"
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(6)

        self.id_label = QLabel(self.sensor_id, self)
        self.name_label = QLabel(self.sensor_name, self)
        self.name_label.setObjectName("SensorName")

        top_layout.addWidget(self.id_label)
        top_layout.addWidget(self.name_label)
        top_layout.addStretch()
        layout.addLayout(top_layout)

        # Bottom line: "1.42 м"
        self.val_label = QLabel(f"{self.value:.2f} м", self)
        self.val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.val_label)

    def set_value(self, value: float):
        self.value = value
        self.val_label.setText(f"{value:.2f} м")

        if value > 1.0:
            color = "#00e676"
            border_color = "#00e676"
            bg = "#03241e"
        elif value >= 0.5:
            color = "#ffb300"
            border_color = "#ffb300"
            bg = "#262208"
        else:
            color = "#f43f5e"
            border_color = "#f43f5e"
            bg = "#290c14"

        self.id_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 13px;")
        self.val_label.setStyleSheet(f"color: {color}; font-weight: 800; font-size: 17px;")
        self.setStyleSheet(f"""
            QFrame#SensorBox {{
                background-color: {bg};
                border: 1px solid {border_color};
                border-radius: 6px;
                min-width: 105px;
            }}
        """)


class SensorsWidget(QFrame):
    sensor_updated = pyqtSignal(int, float)
    sensors_updated = pyqtSignal(list)

    DEFAULT_VALUES = [1.42, 2.86, 0.94, 0.38, 1.18]

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setObjectName("SensorsWidget")
        self.setProperty("class", "card")

        self.values = list(self.DEFAULT_VALUES)
        self.boxes: list[SensorBox] = []

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 10, 14, 10)
        main_layout.setSpacing(6)

        # Title & Subtitle
        header_layout = QVBoxLayout()
        header_layout.setSpacing(1)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("5 датчиків відстані", self)
        title.setObjectName("SensorsTitle")
        header_layout.addWidget(title)

        subtitle = QLabel("Відстань до перешкод у реальному часі", self)
        subtitle.setObjectName("SensorsSubtitle")
        header_layout.addWidget(subtitle)

        main_layout.addLayout(header_layout)

        # Grid visualization area
        grid = QGridLayout()
        grid.setContentsMargins(0, 4, 0, 4)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(6)

        # Sensor Boxes
        self.s1 = SensorBox("S1", "Передній лівий", self.values[0], self)
        self.s2 = SensorBox("S2", "Передній центр", self.values[1], self)
        self.s3 = SensorBox("S3", "Передній правий", self.values[2], self)
        self.s4 = SensorBox("S4", "Лівий бік", self.values[3], self)
        self.s5 = SensorBox("S5", "Правий бік", self.values[4], self)

        self.boxes = [self.s1, self.s2, self.s3, self.s4, self.s5]

        # Car sprite in center
        self.car_label = QLabel(self)
        self.car_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        car_path = Path("assets/images/car_perfect.png")
        if car_path.exists():
            car_pix = QPixmap(str(car_path))
            self.car_label.setPixmap(car_pix.scaled(
                175, 125,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

        grid.addWidget(self.s1, 0, 0, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.s2, 0, 1, Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(self.s3, 0, 2, Qt.AlignmentFlag.AlignRight)

        grid.addWidget(self.s4, 1, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(self.car_label, 1, 1, Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.s5, 1, 2, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        main_layout.addLayout(grid, 1)

        # Bottom Legend Row
        legend_layout = QHBoxLayout()
        legend_layout.setContentsMargins(0, 0, 0, 0)
        legend_layout.setSpacing(18)
        legend_layout.addStretch()

        for col, txt in [("#00e676", "> 1 м"), ("#ffb300", "0.5 – 1 м"), ("#f43f5e", "< 0.5 м")]:
            dot = QLabel("●", self)
            dot.setStyleSheet(f"color: {col}; font-size: 11px;")
            lbl = QLabel(txt, self)
            lbl.setObjectName("LegendText")
            legend_layout.addWidget(dot)
            legend_layout.addWidget(lbl)

        legend_layout.addStretch()
        main_layout.addLayout(legend_layout)

    def _connect_signals(self):
        self.sensor_updated.connect(self.update_sensor)
        self.sensors_updated.connect(self.update_sensors)

    def update_sensor(self, index: int, value: float):
        if 0 <= index < len(self.boxes):
            self.values[index] = value
            self.boxes[index].set_value(value)

    def update_sensors(self, values: list):
        for i, val in enumerate(values):
            if i < len(self.boxes):
                self.update_sensor(i, float(val))
