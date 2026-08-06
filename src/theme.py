"""macOS design tokens, colors, and styles for the application."""

# ── macOS Color Palette ────────────────────────────────────────────────
MACOS_BLUE = "#1976D2"
MACOS_BLUE_HOVER = "#1565C0"
MACOS_BLUE_PRESSED = "#0D47A1"
MACOS_GREEN = "#388E3C"
MACOS_GREEN_HOVER = "#2E7D32"
MACOS_RED = "#D32F2F"
MACOS_RED_HOVER = "#C62828"
MACOS_ORANGE = "#F57C00"
MACOS_GRAY_LIGHT = "#F5F5F5"
MACOS_GRAY_MEDIUM = "#E0E0E0"
MACOS_GRAY_DARK = "#616161"
MACOS_WHITE = "#FFFFFF"
MACOS_TEXT = "#212121"
MACOS_TEXT_SECONDARY = "#616161"
MACOS_BORDER = "#E0E0E0"

# ── Font ────────────────────────────────────────────────────────────────
FONT_FAMILY = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

# ── Button Styles ──────────────────────────────────────────────────────
BIG_BUTTON_STYLE = f"""
    QPushButton {{
        background: {MACOS_BLUE};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 16px 32px;
        font-size: 15px;
        font-weight: 600;
        font-family: {FONT_FAMILY};
        min-width: 180px;
        min-height: 48px;
    }}
    QPushButton:hover {{ background: {MACOS_BLUE_HOVER}; }}
    QPushButton:pressed {{ background: {MACOS_BLUE_PRESSED}; }}
    QPushButton:disabled {{ background: #BDBDBD; color: #757575; }}
"""

SECONDARY_BUTTON_STYLE = f"""
    QPushButton {{
        background: {MACOS_WHITE};
        color: {MACOS_BLUE};
        border: 2px solid {MACOS_BLUE};
        border-radius: 12px;
        padding: 14px 30px;
        font-size: 15px;
        font-weight: 600;
        font-family: {FONT_FAMILY};
        min-width: 180px;
        min-height: 48px;
    }}
    QPushButton:hover {{ background: #E3F2FD; }}
    QPushButton:pressed {{ background: #BBDEFB; }}
"""

DANGER_BUTTON_STYLE = f"""
    QPushButton {{
        background: {MACOS_RED};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 16px 32px;
        font-size: 15px;
        font-weight: 600;
        font-family: {FONT_FAMILY};
        min-width: 180px;
        min-height: 48px;
    }}
    QPushButton:hover {{ background: {MACOS_RED_HOVER}; }}
    QPushButton:pressed {{ background: #B71C1C; }}
"""

# ── Card Styles ────────────────────────────────────────────────────────
CARD_STYLE = f"""
    QFrame {{
        background: {MACOS_WHITE};
        border: 1px solid {MACOS_BORDER};
        border-radius: 8px;
        padding: 20px;
    }}
"""

DASHBOARD_CARD_STYLE = f"""
    QFrame {{
        background: {MACOS_WHITE};
        border: 1px solid {MACOS_BORDER};
        border-radius: 12px;
        padding: 24px;
    }}
"""

# ── Sidebar Styles ─────────────────────────────────────────────────────
SIDEBAR_STYLE = f"""
    QFrame {{
        background: {MACOS_GRAY_LIGHT};
        border-right: 1px solid {MACOS_BORDER};
    }}
"""

SIDEBAR_ITEM_STYLE = f"""
    QPushButton {{
        background: transparent;
        color: {MACOS_TEXT};
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 14px;
        font-weight: 500;
        font-family: {FONT_FAMILY};
        text-align: left;
    }}
    QPushButton:hover {{
        background: {MACOS_GRAY_MEDIUM};
    }}
"""

SIDEBAR_ITEM_SELECTED = f"""
    QPushButton {{
        background: {MACOS_BLUE};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 14px;
        font-weight: 600;
        font-family: {FONT_FAMILY};
        text-align: left;
    }}
"""

# ── Input Styles ────────────────────────────────────────────────────────
INPUT_STYLE = f"""
    QLineEdit, QSpinBox, QComboBox {{
        background: {MACOS_WHITE};
        border: 1px solid {MACOS_BORDER};
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
        font-family: {FONT_FAMILY};
        color: {MACOS_TEXT};
    }}
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border-color: {MACOS_BLUE};
    }}
"""

# ── Label Styles ───────────────────────────────────────────────────────
TITLE_STYLE = f"color: {MACOS_TEXT}; font-size: 22px; font-weight: 700; font-family: {FONT_FAMILY};"
SUBTITLE_STYLE = f"color: {MACOS_TEXT_SECONDARY}; font-size: 13px; font-family: {FONT_FAMILY};"
SECTION_TITLE_STYLE = f"color: {MACOS_TEXT}; font-size: 16px; font-weight: 600; font-family: {FONT_FAMILY};"
