from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from PyQt6.QtCore import pyqtSignal


class SensorsWidget(QFrame):
    sensor_updated = pyqtSignal(int, float)
    sensors_updated = pyqtSignal(list)

    DEFAULT_VALUES = [15.0, 12.5, 8.0, 6.2, 3.5]

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        
        self.setObjectName("SensorsWidget")
        self.setProperty("class", "card")

        self.values = list(self.DEFAULT_VALUES)
        self.value_labels: list[QLabel] = []

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        title = QLabel("Sensors", self)
        title.setObjectName("SensorsTitle")
        layout.addWidget(title)

        for i in range(5):
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)

            name_label = QLabel(f"Sensor {i + 1}", self)
            name_label.setProperty("class", "sensor-name")

            val = self.values[i]
            val_label = QLabel(f"{val:.1f} cm", self)
            val_label.setObjectName(f"SensorValue_{i}")
            val_label.setProperty("class", "sensor-value")
            val_label.setProperty("status", self._get_status(val))

            row_layout.addWidget(name_label)
            row_layout.addWidget(val_label)

            layout.addLayout(row_layout)
            self.value_labels.append(val_label)

    def _connect_signals(self):
        self.sensor_updated.connect(self.update_sensor)
        self.sensors_updated.connect(self.update_sensors)

    @staticmethod
    def _get_status(value: float) -> str:
        if value > 10:
            return "green"
        elif value > 5:
            return "yellow"
        return "red"

    def update_sensor(self, index: int, value: float):
        if 0 <= index < len(self.value_labels):
            self.values[index] = value
            label = self.value_labels[index]
            label.setText(f"{value:.1f} cm")
            label.setProperty("status", self._get_status(value))
            label.style().unpolish(label) # type: ignore
            label.style().polish(label) # type: ignore

    def update_sensors(self, values: list):
        for i, val in enumerate(values):
            if i < len(self.value_labels):
                self.update_sensor(i, float(val))
