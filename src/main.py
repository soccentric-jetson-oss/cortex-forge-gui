"""Cortex Forge GUI - Entry point."""
import sys
from PySide6.QtWidgets import QApplication
from src.app import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Cortex Forge")
    app.setOrganizationName("SoC Centric")
    app.setApplicationVersion("0.1.0")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
