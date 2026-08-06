# SPDX-License-Identifier: MIT
# Copyright (c) 2026 SoC Centric LLC

"""
Main application window for Cortex Forge GUI.

macOS-inspired design with a sidebar navigation and stacked pages:
- Dashboard: real-time accelerator metrics
- Models: model management (load, unload, list)
- Inference: run inference and view results
- Settings: connection configuration
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
    QApplication, QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtGui import QFont, QPalette, QColor

from src.pages.dashboard_page import DashboardPage
from src.pages.models_page import ModelsPage
from src.pages.inference_page import InferencePage
from src.pages.settings_page import SettingsPage
from src.client.grpc_client import GrpcClient


class SidebarButton(QPushButton):
    """Styled sidebar navigation button."""

    def __init__(self, text, icon_text="", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(44)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                color: #212121;
                background: transparent;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.08);
            }
            QPushButton:checked {
                background: rgba(100, 149, 237, 0.25);
                color: #1976D2;
                font-weight: 600;
            }
        """)


class CortexForgeApp(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cortex Forge")
        self.setMinimumSize(1100, 750)
        self.resize(1280, 800)

        # gRPC client
        self.grpc_client = GrpcClient()

        # Setup UI
        self._setup_ui()
        self._setup_connections()

        # Connection timer
        self._conn_timer = QTimer(self)
        self._conn_timer.timeout.connect(self._check_connection)
        self._conn_timer.start(5000)  # Check every 5s

        # Try initial connection
        self._connect_to_server()

    def _setup_ui(self):
        """Build the main window layout."""
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────────────
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border-right: 1px solid #e0e0e0;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        sidebar_layout.setSpacing(4)

        # Logo / Title
        title = QLabel("Cortex Forge")
        title_font = QFont("SF Pro Display", 18, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #1976D2; padding: 0 8px 16px 8px;")
        sidebar_layout.addWidget(title)

        # Navigation buttons
        self.btn_dashboard = SidebarButton("📊  Dashboard")
        self.btn_models = SidebarButton("🧠  Models")
        self.btn_inference = SidebarButton("⚡  Inference")
        self.btn_settings = SidebarButton("⚙️  Settings")

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_models)
        sidebar_layout.addWidget(self.btn_inference)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_settings)

        # ── Content area ─────────────────────────────────────────────────
        content = QFrame()
        content.setStyleSheet("background: #f5f5f5;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage(self.grpc_client)
        self.models_page = ModelsPage(self.grpc_client)
        self.inference_page = InferencePage(self.grpc_client)
        self.settings_page = SettingsPage(self.grpc_client)

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.models_page)
        self.stack.addWidget(self.inference_page)
        self.stack.addWidget(self.settings_page)

        content_layout.addWidget(self.stack)

        # ── Assemble ─────────────────────────────────────────────────────
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content, 1)

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: #ffffff;
                color: #616161;
                border-top: 1px solid #e0e0e0;
                font-size: 12px;
            }
        """)
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Disconnected")
        self.status_bar.addPermanentWidget(self.status_label)

        # Default to dashboard
        self.btn_dashboard.setChecked(True)
        self.stack.setCurrentIndex(0)

    def _setup_connections(self):
        """Connect signals."""
        self.btn_dashboard.clicked.connect(lambda: self._navigate(0))
        self.btn_models.clicked.connect(lambda: self._navigate(1))
        self.btn_inference.clicked.connect(lambda: self._navigate(2))
        self.btn_settings.clicked.connect(lambda: self._navigate(3))

        self.settings_page.connection_changed.connect(self._on_connection_changed)

    def _navigate(self, index):
        """Switch to the given page index."""
        for btn in [self.btn_dashboard, self.btn_models,
                     self.btn_inference, self.btn_settings]:
            btn.setChecked(False)

        {0: self.btn_dashboard,
         1: self.btn_models,
         2: self.btn_inference,
         3: self.btn_settings}[index].setChecked(True)

        self.stack.setCurrentIndex(index)

    def _connect_to_server(self):
        """Attempt to connect to the gRPC server."""
        host = self.settings_page.host
        port = self.settings_page.port
        success = self.grpc_client.connect(host, port)
        if success:
            self.status_label.setText(f"Connected to {host}:{port}")
            self.status_label.setStyleSheet("color: #388E3C;")
        else:
            self.status_label.setText("Disconnected")
            self.status_label.setStyleSheet("color: #D32F2F;")

    def _check_connection(self):
        """Periodic connection health check."""
        if self.grpc_client.is_connected():
            if not self.status_label.text().startswith("Connected"):
                self.status_label.setText(
                    f"Connected to {self.settings_page.host}:{self.settings_page.port}")
                self.status_label.setStyleSheet("color: #388E3C;")
        else:
            self.status_label.setText("Disconnected")
            self.status_label.setStyleSheet("color: #D32F2F;")

    @Slot()
    def _on_connection_changed(self):
        """Handle connection settings change."""
        self._connect_to_server()
