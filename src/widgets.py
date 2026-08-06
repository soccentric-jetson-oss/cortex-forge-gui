"""macOS-style custom widgets.

Provides BigButtonBox, MacCard, StatusIndicator, and other reusable
widgets for building elegant macOS-inspired interfaces.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from src.theme import (
    BIG_BUTTON_STYLE, SECONDARY_BUTTON_STYLE, DANGER_BUTTON_STYLE,
    CARD_STYLE, DASHBOARD_CARD_STYLE,
    TITLE_STYLE, SUBTITLE_STYLE, SECTION_TITLE_STYLE,
    MACOS_TEXT, MACOS_TEXT_SECONDARY, MACOS_BLUE, MACOS_GREEN, MACOS_RED,
)


class BigButtonBox(QFrame):
    """A card containing a title, description, and large action button.

    Provides an elegant, macOS-style call-to-action card.
    """

    def __init__(self, title: str, description: str, button_text: str,
                 button_style: str = "primary", parent=None):
        super().__init__(parent)
        self.setStyleSheet(DASHBOARD_CARD_STYLE)
        self.setMinimumHeight(160)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(SECTION_TITLE_STYLE)
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet(SUBTITLE_STYLE)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        layout.addStretch()

        # Button
        self.button = QPushButton(button_text)
        self.button.setCursor(Qt.PointingHandCursor)
        if button_style == "primary":
            self.button.setStyleSheet(BIG_BUTTON_STYLE)
        elif button_style == "secondary":
            self.button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        elif button_style == "danger":
            self.button.setStyleSheet(DANGER_BUTTON_STYLE)
        layout.addWidget(self.button, alignment=Qt.AlignLeft)


class MacCard(QFrame):
    """A data display card with title, value, and optional unit.

    Used in dashboards to display metrics like FPS, latency, etc.
    """

    def __init__(self, title: str, value: str = "--", unit: str = "",
                 color: str = MACOS_BLUE, parent=None):
        super().__init__(parent)
        self.setStyleSheet(CARD_STYLE)
        self.setMinimumSize(200, 100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"color: {MACOS_TEXT_SECONDARY}; font-size: 12px; font-weight: 500;"
        )
        layout.addWidget(title_label)

        # Value row
        value_row = QHBoxLayout()
        value_row.setSpacing(4)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(
            f"color: {color}; font-size: 28px; font-weight: 700;"
        )
        value_row.addWidget(self.value_label)

        if unit:
            unit_label = QLabel(unit)
            unit_label.setStyleSheet(
                f"color: {MACOS_TEXT_SECONDARY}; font-size: 14px; font-weight: 500; padding-top: 8px;"
            )
            value_row.addWidget(unit_label)

        value_row.addStretch()
        layout.addLayout(value_row)

    def set_value(self, value: str):
        """Update the displayed value."""
        self.value_label.setText(value)


class StatusIndicator(QFrame):
    """A small colored dot indicating connection or operational status."""

    def __init__(self, color: str = MACOS_RED, size: int = 12, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.setStyleSheet(
            f"background: {color}; border-radius: {size // 2}px;"
        )

    def set_color(self, color: str):
        """Update the indicator color."""
        self.setStyleSheet(
            f"background: {color}; border-radius: {self.width() // 2}px;"
        )
