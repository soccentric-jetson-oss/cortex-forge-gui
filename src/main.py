# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cortex Forge Contributors

"""
Application entry point. Starts the PySide6 main window.
"""

import sys
from src.app import CortexForgeApp
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Cortex Forge")
    app.setOrganizationName("SoC Centric")
    app.setApplicationVersion("0.1.0")

    window = CortexForgeApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
