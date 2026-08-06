# SPDX-License-Identifier: MIT
# Copyright (c) 2026 SoC Centric LLC

"""
Models page - model management (load, unload, list).
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox,
    QHeaderView, QFrame, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont


class ModelsPage(QWidget):
    """Model management page."""

    def __init__(self, grpc_client, parent=None):
        super().__init__(parent)
        self.grpc_client = grpc_client
        self._setup_ui()

        # Refresh timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(3000)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("Models")
        header.setStyleSheet("color: #e0e0e0; font-size: 28px; font-weight: bold;")
        header.setFont(QFont("SF Pro Display", 28, QFont.Weight.Bold))
        layout.addWidget(header)

        subtitle = QLabel("Load, unload, and manage ML models")
        subtitle.setStyleSheet("color: #888; font-size: 14px;")
        layout.addWidget(subtitle)

        # Controls
        controls = QHBoxLayout()
        controls.setSpacing(12)

        self.load_btn = QPushButton("+ Load Model")
        self.load_btn.setFixedHeight(36)
        self.load_btn.setCursor(Qt.PointingHandCursor)
        self.load_btn.setStyleSheet("""
            QPushButton {
                background: #64b5f6;
                color: #0f0f1a;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background: #90caf9; }
            QPushButton:pressed { background: #42a5f5; }
        """)
        self.load_btn.clicked.connect(self._load_model)
        controls.addWidget(self.load_btn)

        self.unload_btn = QPushButton("✕ Unload Selected")
        self.unload_btn.setFixedHeight(36)
        self.unload_btn.setCursor(Qt.PointingHandCursor)
        self.unload_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #ef5350;
                border: 1px solid #ef5350;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background: #ef535020; }
        """)
        self.unload_btn.clicked.connect(self._unload_model)
        controls.addWidget(self.unload_btn)

        controls.addStretch()
        layout.addLayout(controls)

        # Model table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Model ID", "Name", "Framework", "Accelerator",
            "Batch", "Inferences", "Avg Latency"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background: #1a1a2e;
                border: 1px solid #2a2a4a;
                border-radius: 12px;
                color: #e0e0e0;
                font-size: 12px;
                gridline-color: #2a2a4a;
            }
            QTableWidget::item { padding: 8px; }
            QTableWidget::item:selected { background: #64b5f640; }
            QHeaderView::section {
                background: #0f0f1a;
                color: #888;
                border: none;
                padding: 10px;
                font-weight: 600;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.table)

    def _refresh(self):
        """Refresh the model list."""
        models = self.grpc_client.list_models()
        self.table.setRowCount(len(models))

        for i, model in enumerate(models):
            self.table.setItem(i, 0, QTableWidgetItem(model.get("model_id", "")))
            self.table.setItem(i, 1, QTableWidgetItem(model.get("model_name", "")))
            self.table.setItem(i, 2, QTableWidgetItem(model.get("framework", "")))
            self.table.setItem(i, 3, QTableWidgetItem(model.get("accelerator", "")))
            self.table.setItem(i, 4, QTableWidgetItem(str(model.get("batch_size", 1))))
            self.table.setItem(i, 5, QTableWidgetItem(str(model.get("total_inferences", 0))))
            avg_lat = model.get("avg_latency_us", 0)
            self.table.setItem(i, 6, QTableWidgetItem(f"{avg_lat:.0f} μs"))

    def _load_model(self):
        """Open file dialog and load a model."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Model File", "",
            "Model Files (*.engine *.onnx *.plan *.trt);;All Files (*)"
        )
        if not file_path:
            return

        result = self.grpc_client.load_model(file_path)
        if result and result.get("success"):
            QMessageBox.information(
                self, "Model Loaded",
                f"Model loaded successfully.\nID: {result['model_id']}\nName: {result['model_name']}"
            )
            self._refresh()
        else:
            error = result.get("error", "Unknown error") if result else "Connection failed"
            QMessageBox.warning(self, "Load Failed", f"Failed to load model:\n{error}")

    def _unload_model(self):
        """Unload the selected model."""
        current = self.table.currentRow()
        if current < 0:
            QMessageBox.information(self, "No Selection", "Please select a model to unload.")
            return

        model_id = self.table.item(current, 0).text()
        reply = QMessageBox.question(
            self, "Confirm Unload",
            f"Unload model {model_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success = self.grpc_client.unload_model(model_id)
            if success:
                self._refresh()
            else:
                QMessageBox.warning(self, "Unload Failed", "Failed to unload model.")
