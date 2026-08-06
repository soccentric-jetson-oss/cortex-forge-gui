# SPDX-License-Identifier: MIT
# Copyright (c) 2026 SoC Centric LLC

"""
Settings page - connection configuration.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QSpinBox, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class SettingsPage(QWidget):
    """Settings page for server connection configuration."""

    connection_changed = Signal()

    def __init__(self, grpc_client, parent=None):
        super().__init__(parent)
        self.grpc_client = grpc_client
        self.host = "localhost"
        self.port = 50051
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("Settings")
        header.setStyleSheet("color: #212121; font-size: 28px; font-weight: bold;")
        header.setFont(QFont("SF Pro Display", 28, QFont.Weight.Bold))
        layout.addWidget(header)

        subtitle = QLabel("Configure the Cortex Forge server connection")
        subtitle.setStyleSheet("color: #616161; font-size: 14px;")
        layout.addWidget(subtitle)

        # Connection settings card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 24px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)

        # Host
        host_layout = QHBoxLayout()
        host_label = QLabel("Server Host:")
        host_label.setFixedWidth(120)
        host_label.setStyleSheet("color: #ccc; font-size: 13px;")
        host_layout.addWidget(host_label)

        self.host_input = QLineEdit("localhost")
        self.host_input.setStyleSheet("""
            QLineEdit {
                background: #f5f5f5;
                color: #212121;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus { border-color: #1976D2; }
        """)
        host_layout.addWidget(self.host_input, 1)
        card_layout.addLayout(host_layout)

        # Port
        port_layout = QHBoxLayout()
        port_label = QLabel("Server Port:")
        port_label.setFixedWidth(120)
        port_label.setStyleSheet("color: #ccc; font-size: 13px;")
        port_layout.addWidget(port_label)

        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        self.port_input.setValue(50051)
        self.port_input.setFixedWidth(120)
        self.port_input.setStyleSheet("""
            QSpinBox {
                background: #f5f5f5;
                color: #212121;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QSpinBox:focus { border-color: #1976D2; }
        """)
        port_layout.addWidget(self.port_input)
        port_layout.addStretch()
        card_layout.addLayout(port_layout)

        # Connect button
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setFixedHeight(36)
        self.connect_btn.setCursor(Qt.PointingHandCursor)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background: #1976D2;
                color: #212121;
                border: none;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background: #90caf9; }
        """)
        self.connect_btn.clicked.connect(self._connect)
        card_layout.addWidget(self.connect_btn)

        layout.addWidget(card)

        # Status
        self.status_label = QLabel("Not connected")
        self.status_label.setStyleSheet("color: #616161; font-size: 12px;")
        layout.addWidget(self.status_label)

        layout.addStretch()

    def _connect(self):
        """Connect to the server with current settings."""
        self.host = self.host_input.text().strip()
        self.port = self.port_input.value()

        success = self.grpc_client.connect(self.host, self.port)
        if success:
            self.status_label.setText(f"✅ Connected to {self.host}:{self.port}")
            self.status_label.setStyleSheet("color: #388E3C; font-size: 12px;")
        else:
            self.status_label.setText(f"❌ Failed to connect to {self.host}:{self.port}")
            self.status_label.setStyleSheet("color: #D32F2F; font-size: 12px;")

        self.connection_changed.emit()
