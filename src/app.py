"""Cortex Forge GUI - Main application window.

macOS-style design with complete menu bar, sidebar navigation,
and stacked pages for ML inference control.
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QMessageBox
from PySide6.QtCore import QTimer
from src.client.client import CortexForgeClient
from src.sidebar import SidebarWidget
from src.menu import setup_menu_bar
from src.pages.dashboard import DashboardPage
from src.pages.controls import ControlsPage
from src.pages.settings import SettingsPage


class MainWindow(QMainWindow):
    """Main application window with menu bar, sidebar, and stacked pages."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cortex Forge")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)
        self._client = CortexForgeClient()
        setup_menu_bar(self)

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.sidebar = SidebarWidget()
        self.pages = QStackedWidget()
        self.pages.addWidget(DashboardPage(self._client))
        self.pages.addWidget(ControlsPage(self._client))
        self.pages.addWidget(SettingsPage(self._client))
        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)
        self.setCentralWidget(central)
        self.sidebar.navigation_changed.connect(self.pages.setCurrentIndex)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(2000)
        self._client.connect()
        self.sidebar.set_connected(self._client.connected)

    def navigate_to(self, index: int):
        self.pages.setCurrentIndex(index)
        self.sidebar._on_navigate(index)

    def on_new_connection(self): self.navigate_to(2)
    def on_undo(self): pass
    def on_redo(self): pass
    def on_cut(self): pass
    def on_copy(self): pass
    def on_paste(self): pass
    def on_select_all(self): pass
    def on_toggle_fullscreen(self):
        if self.isFullScreen(): self.showNormal()
        else: self.showFullScreen()
    def on_toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())
    def on_connect(self): self._client.connect(); self.sidebar.set_connected(self._client.connected)
    def on_disconnect(self): self._client.disconnect(); self.sidebar.set_connected(False)
    def on_refresh(self): self._refresh()
    def on_export_data(self): QMessageBox.information(self, "Export", "Export feature coming soon.")
    def on_about(self): QMessageBox.about(self, "About Cortex Forge", "Cortex Forge v0.1.0\n\nML Inference Control for NVIDIA Jetson AGX Orin\n\nCopyright (c) 2026 SoC Centric LLC")
    def on_documentation(self): QMessageBox.information(self, "Documentation", "See docs/ folder.")
    def on_report_issue(self): QMessageBox.information(self, "Report Issue", "github.com/soccentric-jetson-oss/cortex-forge-gui")

    def _refresh(self):
        if not self._client.connected:
            self._client.connect()
            self.sidebar.set_connected(self._client.connected)
            return
        self.dashboard_page.refresh()
