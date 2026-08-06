"""Settings page for Cortex Forge connection configuration."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame
from src.theme import TITLE_STYLE, SUBTITLE_STYLE, SECTION_TITLE_STYLE, BIG_BUTTON_STYLE, CARD_STYLE, INPUT_STYLE, MACOS_RED, MACOS_GREEN


class SettingsPage(QWidget):
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self._client = client
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        header = QLabel("Settings")
        header.setStyleSheet(TITLE_STYLE)
        layout.addWidget(header)
        desc = QLabel("Configure server connection.")
        desc.setStyleSheet(SUBTITLE_STYLE)
        layout.addWidget(desc)

        frame = QFrame()
        frame.setStyleSheet(CARD_STYLE)
        fl = QVBoxLayout(frame)
        fl.setSpacing(12)
        fl.addWidget(QLabel("Server Connection"))
        fl.itemAt(fl.count()-1).widget().setStyleSheet(SECTION_TITLE_STYLE)
        addr_row = QHBoxLayout()
        addr_row.addWidget(QLabel("Address:"))
        self.addr_input = QLineEdit("localhost:50051")
        self.addr_input.setStyleSheet(INPUT_STYLE)
        self.addr_input.setMinimumWidth(300)
        addr_row.addWidget(self.addr_input)
        addr_row.addStretch()
        fl.addLayout(addr_row)
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setStyleSheet(BIG_BUTTON_STYLE)
        self.connect_btn.clicked.connect(lambda: self._client.connect())
        fl.addWidget(self.connect_btn)
        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet(f"color: {MACOS_RED}; font-size: 13px;")
        fl.addWidget(self.status_label)
        layout.addWidget(frame)
        layout.addStretch()
