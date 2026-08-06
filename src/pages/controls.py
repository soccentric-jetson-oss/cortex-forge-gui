"""Controls page for Cortex Forge model and accelerator configuration."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QFrame, QHBoxLayout
from PySide6.QtCore import Qt
from src.theme import TITLE_STYLE, SUBTITLE_STYLE, SECTION_TITLE_STYLE, BIG_BUTTON_STYLE, CARD_STYLE, INPUT_STYLE


class ControlsPage(QWidget):
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self._client = client
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        header = QLabel("Controls")
        header.setStyleSheet(TITLE_STYLE)
        layout.addWidget(header)
        desc = QLabel("Configure inference models and accelerator selection.")
        desc.setStyleSheet(SUBTITLE_STYLE)
        layout.addWidget(desc)

        frame = QFrame()
        frame.setStyleSheet(CARD_STYLE)
        fl = QVBoxLayout(frame)
        fl.setSpacing(12)
        fl.addWidget(QLabel("Accelerator Selection"))
        fl[-1].setStyleSheet(SECTION_TITLE_STYLE) if hasattr(fl, '__getitem__') else None
        self.accel_combo = QComboBox()
        self.accel_combo.addItems(["Auto", "GPU", "NVDLA 0", "NVDLA 1", "PVA"])
        self.accel_combo.setStyleSheet(INPUT_STYLE)
        fl.addWidget(self.accel_combo)
        layout.addWidget(frame)
        layout.addStretch()
