# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cortex Forge Contributors

"""
Dashboard page - real-time accelerator metrics visualization.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont


class MetricCard(QFrame):
    """A card displaying a single metric value."""

    def __init__(self, title, value="--", unit="", color="#64b5f6", parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 120)
        self.setStyleSheet(f"""
            QFrame {{
                background: #1a1a2e;
                border: 1px solid #2a2a4a;
                border-radius: 12px;
                padding: 16px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #888; font-size: 11px; font-weight: 600;")
        title_label.setFont(QFont("SF Pro Display", 11))
        layout.addWidget(title_label)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        self.value_label.setFont(QFont("SF Pro Display", 28, QFont.Weight.Bold))
        layout.addWidget(self.value_label)

        self.unit_label = QLabel(unit)
        self.unit_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.unit_label)

    def set_value(self, value):
        self.value_label.setText(str(value))


class AcceleratorGauge(QFrame):
    """Gauge showing accelerator utilization."""

    def __init__(self, name, color="#64b5f6", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: #1a1a2e;
                border: 1px solid #2a2a4a;
                border-radius: 12px;
                padding: 16px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 20)
        layout.setSpacing(8)

        # Name
        name_label = QLabel(name)
        name_label.setStyleSheet("color: #ccc; font-size: 13px; font-weight: 600;")
        name_label.setFont(QFont("SF Pro Display", 13, QFont.Weight.Semibold))
        layout.addWidget(name_label)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setFixedHeight(20)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                background: #2a2a4a;
                border: none;
                border-radius: 10px;
                text-align: center;
                color: white;
                font-size: 11px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}40, stop:1 {color});
                border-radius: 10px;
            }}
        """)
        layout.addWidget(self.progress)

        # Value label
        self.value_label = QLabel("0%")
        self.value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        self.value_label.setFont(QFont("SF Pro Display", 24, QFont.Weight.Bold))
        layout.addWidget(self.value_label)

    def set_value(self, percent):
        self.progress.setValue(int(percent))
        self.value_label.setText(f"{percent:.0f}%")


class DashboardPage(QWidget):
    """Dashboard page showing real-time accelerator metrics."""

    def __init__(self, grpc_client, parent=None):
        super().__init__(parent)
        self.grpc_client = grpc_client
        self._setup_ui()

        # Refresh timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(2000)  # Refresh every 2s

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)

        # Header
        header = QLabel("Dashboard")
        header.setStyleSheet("color: #e0e0e0; font-size: 28px; font-weight: bold;")
        header.setFont(QFont("SF Pro Display", 28, QFont.Weight.Bold))
        layout.addWidget(header)

        subtitle = QLabel("Real-time accelerator utilization and inference metrics")
        subtitle.setStyleSheet("color: #888; font-size: 14px;")
        layout.addWidget(subtitle)

        # Accelerator gauges
        gauge_layout = QHBoxLayout()
        gauge_layout.setSpacing(16)

        self.gpu_gauge = AcceleratorGauge("GPU (Ampere)", "#76ff03")
        self.dla0_gauge = AcceleratorGauge("NVDLA 0", "#64b5f6")
        self.dla1_gauge = AcceleratorGauge("NVDLA 1", "#64b5f6")
        self.pva_gauge = AcceleratorGauge("PVA v2.0", "#ff6d00")

        gauge_layout.addWidget(self.gpu_gauge)
        gauge_layout.addWidget(self.dla0_gauge)
        gauge_layout.addWidget(self.dla1_gauge)
        gauge_layout.addWidget(self.pva_gauge)
        layout.addLayout(gauge_layout)

        # Metrics cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        self.inferences_card = MetricCard("Total Inferences", "0", "", "#76ff03")
        self.latency_card = MetricCard("Avg Latency", "0", "μs", "#64b5f6")
        self.p99_card = MetricCard("P99 Latency", "0", "μs", "#ff6d00")
        self.throughput_card = MetricCard("Throughput", "0", "inf/s", "#ce93d8")

        cards_layout.addWidget(self.inferences_card)
        cards_layout.addWidget(self.latency_card)
        cards_layout.addWidget(self.p99_card)
        cards_layout.addWidget(self.throughput_card)
        layout.addLayout(cards_layout)

        # Memory card
        mem_layout = QHBoxLayout()
        self.mem_card = MetricCard("GPU Memory", "0 / 0", "MB", "#64b5f6")
        mem_layout.addWidget(self.mem_card)
        mem_layout.addStretch()
        layout.addLayout(mem_layout)

        layout.addStretch()

    def _refresh(self):
        """Fetch and display latest metrics."""
        metrics = self.grpc_client.get_metrics()
        if not metrics:
            return

        self.gpu_gauge.set_value(metrics.get("gpu_util_percent", 0))
        self.dla0_gauge.set_value(metrics.get("dla0_util_percent", 0))
        self.dla1_gauge.set_value(metrics.get("dla1_util_percent", 0))
        self.pva_gauge.set_value(metrics.get("pva_util_percent", 0))

        self.inferences_card.set_value(str(metrics.get("total_inferences", 0)))
        self.latency_card.set_value(f"{metrics.get('avg_latency_us', 0):.0f}")
        self.p99_card.set_value(f"{metrics.get('p99_latency_us', 0):.0f}")
        self.throughput_card.set_value(str(metrics.get("inferences_per_second", 0)))

        used = metrics.get("gpu_mem_used_mb", 0)
        total = metrics.get("gpu_mem_total_mb", 0)
        self.mem_card.set_value(f"{used} / {total}")
