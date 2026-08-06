# SPDX-License-Identifier: MIT
"""
Cortex Forge GUI - Application entry point.

Thin entry point that creates the QApplication and launches the
main window. All UI logic lives in src.app.CortexForgeApp.
"""

import sys
from src.app import CortexForgeApp
from PySide6.QtWidgets import QApplication


def main():
    """Create and run the Cortex Forge GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Cortex Forge")
    app.setOrganizationName("SoC Centric")
    app.setApplicationVersion("0.1.0")

    window = CortexForgeApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
