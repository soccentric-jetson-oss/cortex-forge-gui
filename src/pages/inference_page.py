# SPDX-License-Identifier: MIT
# Copyright (c) 2026 SoC Centric LLC

"""
Inference page - run inference and view results.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QComboBox, QFrame, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont


class InferencePage(QWidget):
    """Inference page for running model inference."""

    def __init__(self, grpc_client, parent=None):
        super().__init__(parent)
        self.grpc_client = grpc_client
        self._setup_ui()

        # Refresh model list
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._refresh_models)
        self._refresh_timer.start(5000)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("Inference")
        header.setStyleSheet("color: #e0e0e0; font-size: 28px; font-weight: bold;")
        header.setFont(QFont("SF Pro Display", 28, QFont.Weight.Bold))
        layout.addWidget(header)

        subtitle = QLabel("Run inference on loaded models and view results")
        subtitle.setStyleSheet("color: #888; font-size: 14px;")
        layout.addWidget(subtitle)

        # Model selector
        selector_layout = QHBoxLayout()
        selector_layout.setSpacing(12)

        model_label = QLabel("Model:")
        model_label.setStyleSheet("color: #ccc; font-size: 13px;")
        selector_layout.addWidget(model_label)

        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(300)
        self.model_combo.setStyleSheet("""
            QComboBox {
                background: #1a1a2e;
                color: #e0e0e0;
                border: 1px solid #2a2a4a;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QComboBox QAbstractItemView {
                background: #1a1a2e;
                color: #e0e0e0;
                border: 1px solid #2a2a4a;
                selection-background-color: #64b5f640;
            }
        """)
        selector_layout.addWidget(self.model_combo)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)

        # Run button
        self.run_btn = QPushButton("▶  Run Inference")
        self.run_btn.setFixedHeight(40)
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.setStyleSheet("""
            QPushButton {
                background: #76ff03;
                color: #0f0f1a;
                border: none;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { background: #9cff57; }
            QPushButton:pressed { background: #64dd17; }
            QPushButton:disabled { background: #333; color: #666; }
        """)
        self.run_btn.clicked.connect(self._run_inference)
        layout.addWidget(self.run_btn)

        # Progress
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Indeterminate
        self.progress.setFixedHeight(4)
        self.progress.setStyleSheet("""
            QProgressBar {
                background: #2a2a4a;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: #64b5f6;
                border-radius: 2px;
            }
        """)
        self.progress.hide()
        layout.addWidget(self.progress)

        # Results
        results_label = QLabel("Results:")
        results_label.setStyleSheet("color: #ccc; font-size: 13px; font-weight: 600;")
        layout.addWidget(results_label)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet("""
            QTextEdit {
                background: #1a1a2e;
                color: #e0e0e0;
                border: 1px solid #2a2a4a;
                border-radius: 12px;
                padding: 16px;
                font-size: 12px;
                font-family: 'SF Mono', 'Consolas', monospace;
            }
        """)
        layout.addWidget(self.results_text, 1)

    def _refresh_models(self):
        """Update the model selector with loaded models."""
        current = self.model_combo.currentText()
        self.model_combo.clear()

        models = self.grpc_client.list_models()
        for model in models:
            name = f"{model.get('model_name', '')} ({model.get('model_id', '')})"
            self.model_combo.addItem(name, model.get("model_id"))

        # Restore selection
        idx = self.model_combo.findText(current)
        if idx >= 0:
            self.model_combo.setCurrentIndex(idx)

    def _run_inference(self):
        """Run inference on the selected model."""
        model_id = self.model_combo.currentData()
        if not model_id:
            self.results_text.setText("Please select a model first.")
            return

        self.run_btn.setEnabled(False)
        self.progress.show()

        result = self.grpc_client.infer(model_id)

        self.progress.hide()
        self.run_btn.setEnabled(True)

        if result and result.get("success"):
            text = (
                f"✅ Inference Complete\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Latency: {result.get('latency_us', 0)} μs\n"
                f"Output size: {len(result.get('output_data', b''))} bytes\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Output (hex): {result.get('output_data', b'')[:64].hex()}\n"
            )
            self.results_text.setText(text)
        else:
            error = result.get("error", "Unknown error") if result else "Connection failed"
            self.results_text.setText(f"❌ Inference Failed\n{error}")
