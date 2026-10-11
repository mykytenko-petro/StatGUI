from pathlib import Path
from PyQt6.QtWidgets import QApplication


def set_styles(app: QApplication, styles_dir: str = "assets/styles"):
    styles_path = Path(styles_dir)

    qss_files = sorted(styles_path.rglob("*.qss"))

    combined_styles = []
    for file in qss_files:
        with open(file, "r", encoding="utf-8") as f:
            combined_styles.append(f.read())

    app.setStyleSheet("\n".join(combined_styles))