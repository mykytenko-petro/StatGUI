from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)
from PyQt6.QtCore import Qt


class EventRow(QWidget):
    def __init__(self, time_str: str, message: str, parent: QWidget | None = None, is_last: bool = False):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(6, 4, 6, 4)
        row_layout.setSpacing(10)

        dot = QLabel("●", self)
        dot.setObjectName("EventDot")
        row_layout.addWidget(dot)

        time_lbl = QLabel(time_str, self)
        time_lbl.setObjectName("EventTime")
        row_layout.addWidget(time_lbl)

        msg_lbl = QLabel(message, self)
        msg_lbl.setObjectName("EventMessage")
        row_layout.addWidget(msg_lbl, 1)

        layout.addLayout(row_layout)

        if not is_last:
            sep = QFrame(self)
            sep.setObjectName("EventRowSeparator")
            sep.setFixedHeight(1)
            layout.addWidget(sep)


class EventsWidget(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setObjectName("EventsWidget")
        self.setProperty("class", "card")

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        # Header
        title = QLabel("Події", self)
        title.setObjectName("EventsTitle")
        layout.addWidget(title)

        # Events list card
        list_card = QFrame(self)
        list_card.setObjectName("EventsListCard")
        list_layout = QVBoxLayout(list_card)
        list_layout.setContentsMargins(6, 6, 6, 6)
        list_layout.setSpacing(0)

        events_data = [
            ("17:14:46", "Телеметрію активовано"),
            ("17:14:43", "Калібрування завершено"),
            ("17:14:38", "Камеру підключено"),
            ("17:14:31", "BOLID-01 онлайн"),
        ]

        for i, (t, msg) in enumerate(events_data):
            is_last = (i == len(events_data) - 1)
            row = EventRow(t, msg, list_card, is_last=is_last)
            list_layout.addWidget(row)

        layout.addWidget(list_card, 1)

        # Open Log Button
        self.log_btn = QPushButton("Відкрити журнал   →", self)
        self.log_btn.setObjectName("OpenLogButton")
        layout.addWidget(self.log_btn)
