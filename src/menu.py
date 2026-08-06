"""macOS-style menu bar builder.

Provides a complete menu bar with File, Edit, View, Tools, and Help menus.
Each menu has standard macOS items with keyboard shortcuts.
"""

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMenuBar


def setup_menu_bar(window) -> QMenuBar:
    """Build and attach a complete macOS-style menu bar to the given window.

    Args:
        window: QMainWindow instance with handler methods (on_*, toggle_*)

    Returns:
        The configured QMenuBar instance.
    """
    menubar = window.menuBar()

    # ── File Menu ───────────────────────────────────────────────────────
    file_menu = menubar.addMenu("&File")
    _add_action(file_menu, "&New Connection", window.on_new_connection, "Ctrl+N")
    _add_action(file_menu, "&Close Window", window.close, "Ctrl+W")
    file_menu.addSeparator()
    _add_action(file_menu, "&Quit", window.close, "Ctrl+Q")

    # ── Edit Menu ──────────────────────────────────────────────────────
    edit_menu = menubar.addMenu("&Edit")
    _add_action(edit_menu, "&Undo", window.on_undo, "Ctrl+Z")
    _add_action(edit_menu, "&Redo", window.on_redo, "Ctrl+Shift+Z")
    edit_menu.addSeparator()
    _add_action(edit_menu, "Cu&t", window.on_cut, "Ctrl+X")
    _add_action(edit_menu, "&Copy", window.on_copy, "Ctrl+C")
    _add_action(edit_menu, "&Paste", window.on_paste, "Ctrl+V")
    _add_action(edit_menu, "Select &All", window.on_select_all, "Ctrl+A")

    # ── View Menu ──────────────────────────────────────────────────────
    view_menu = menubar.addMenu("&View")
    _add_action(view_menu, "&Dashboard", lambda: window.navigate_to(0), "Ctrl+1")
    _add_action(view_menu, "&Controls", lambda: window.navigate_to(1), "Ctrl+2")
    _add_action(view_menu, "&Settings", lambda: window.navigate_to(2), "Ctrl+3")
    view_menu.addSeparator()
    _add_action(view_menu, "Toggle &Full Screen", window.on_toggle_fullscreen, "Ctrl+Shift+F")
    _add_action(view_menu, "Toggle &Sidebar", window.on_toggle_sidebar, "Ctrl+\\")

    # ── Tools Menu ─────────────────────────────────────────────────────
    tools_menu = menubar.addMenu("&Tools")
    _add_action(tools_menu, "&Connect", window.on_connect, "Ctrl+D")
    _add_action(tools_menu, "&Disconnect", window.on_disconnect, "Ctrl+Shift+D")
    _add_action(tools_menu, "&Refresh", window.on_refresh, "Ctrl+R")
    tools_menu.addSeparator()
    _add_action(tools_menu, "&Export Data", window.on_export_data, "Ctrl+E")

    # ── Help Menu ──────────────────────────────────────────────────────
    help_menu = menubar.addMenu("&Help")
    _add_action(help_menu, "&About", window.on_about)
    _add_action(help_menu, "&Documentation", window.on_documentation, "F1")
    _add_action(help_menu, "Report &Issue", window.on_report_issue)

    return menubar


def _add_action(menu, label, handler, shortcut=None):
    """Add an action to a menu with optional keyboard shortcut."""
    action = QAction(label, menu.parent())
    action.triggered.connect(handler)
    if shortcut:
        action.setShortcut(QKeySequence(shortcut))
    menu.addAction(action)
