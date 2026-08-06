"""macOS-style sidebar navigation widget.

Provides a fixed-width sidebar with icon + label navigation items,
a title header, and a connection status indicator at the bottom.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Signal, Qt
from src.theme import SIDEBAR_STYLE, SIDEBAR_ITEM_STYLE, SIDEBAR_ITEM_SELECTED, MACOS_BLUE, MACOS_GREEN, MACOS_RED


class SidebarWidget(QFrame):
    """macOS-style sidebar with icon + label navigation items.

    Emits navigation_changed(page_index) when a nav item is clicked.
    """

    navigation_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setStyleSheet(SIDEBAR_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 12)
        layout.setSpacing(4)

        # ── App title ──────────────────────────────────────────────────
        title = QLabel("Cortex Forge")
        title.setStyleSheet(
            f"color: {MACOS_BLUE}; font-size: 18px; font-weight: 700; "
            "padding: 0 4px 16px 4px;"
        )
        layout.addWidget(title)

        # ── Navigation items ───────────────────────────────────────────
        self._buttons = []
        self._current_index = 0

        items = [
            ("📊", "Dashboard"),
            ("🎛", "Controls"),
            ("⚙", "Settings"),
        ]

        for i, (icon, label) in enumerate(items):
            btn = QPushButton(f"  {icon}  {label}")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(44)
            btn.clicked.connect(lambda checked, idx=i: self._on_navigate(idx))
            self._buttons.append(btn)
            layout.addWidget(btn)

        # ── Spacer ─────────────────────────────────────────────────────
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # ── Connection status ──────────────────────────────────────────
        self.status_label = QLabel("  ●  Disconnected")
        self.status_label.setStyleSheet(
            f"color: {MACOS_RED}; font-size: 12px; padding: 8px 4px;"
        )
        layout.addWidget(self.status_label)

        # Set initial selection
        self._update_selection()

    def _on_navigate(self, index: int):
        """Handle navigation button click."""
        self._current_index = index
        self._update_selection()
        self.navigation_changed.emit(index)

    def _update_selection(self):
        """Update button styles to reflect current selection."""
        for i, btn in enumerate(self._buttons):
            if i == self._current_index:
                btn.setStyleSheet(SIDEBAR_ITEM_SELECTED)
            else:
                btn.setStyleSheet(SIDEBAR_ITEM_STYLE)

    def set_connected(self, connected: bool):
        """Update the connection status indicator."""
        if connected:
            self.status_label.setText("  ●  Connected")
            self.status_label.setStyleSheet(
                f"color: {MACOS_GREEN}; font-size: 12px; padding: 8px 4px;"
            )
        else:
            self.status_label.setText("  ●  Disconnected")
            self.status_label.setStyleSheet(
                f"color: {MACOS_RED}; font-size: 12px; padding: 8px 4px;"
            )
