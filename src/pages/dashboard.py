"""Dashboard page for Cortex Forge ML inference control."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from src.theme import TITLE_STYLE, SUBTITLE_STYLE
from src.widgets import BigButtonBox, MacCard


class DashboardPage(QWidget):
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self._client = client
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)

        header = QLabel("Dashboard")
        header.setStyleSheet(TITLE_STYLE)
        layout.addWidget(header)
        desc = QLabel("Monitor and control ML inference on Jetson AGX Orin accelerators.")
        desc.setStyleSheet(SUBTITLE_STYLE)
        layout.addWidget(desc)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        self.infer_box = BigButtonBox("Run Inference", "Execute model inference on the selected accelerator.\nConfigure model and parameters in Controls.", "▶  Run Inference", "primary")
        btn_row.addWidget(self.infer_box)
        self.stop_box = BigButtonBox("Stop", "Halt the currently running inference task.\nAll accelerator resources will be released.", "■  Stop", "danger")
        btn_row.addWidget(self.stop_box)
        layout.addLayout(btn_row)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)
        self.status_card = MacCard("Status", "Idle", "", "#616161")
        self.latency_card = MacCard("Latency", "0", "ms")
        self.throughput_card = MacCard("Throughput", "0", "inf/s")
        self.model_card = MacCard("Model", "None", "")
        cards_row.addWidget(self.status_card)
        cards_row.addWidget(self.latency_card)
        cards_row.addWidget(self.throughput_card)
        cards_row.addWidget(self.model_card)
        layout.addLayout(cards_row)
        layout.addStretch()

    def refresh(self):
        if not self._client.connected: return
        metrics = self._client.get_metrics()
        self.latency_card.set_value(str(int(metrics.get("avg_latency_us", 0))))
        self.throughput_card.set_value(str(int(metrics.get("inferences_per_second", 0))))
