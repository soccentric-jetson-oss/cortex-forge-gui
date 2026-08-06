# SPDX-License-Identifier: MIT
# Copyright (c) 2026 SoC Centric LLC

"""
Protobuf model definitions for Cortex Forge.

These are generated from proto/cortex_forge.proto.
This file provides type hints and model wrappers.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ModelInfo:
    """Information about a loaded model."""
    model_id: str = ""
    model_name: str = ""
    framework: str = ""
    batch_size: int = 1
    accelerator: str = "auto"
    load_time_us: int = 0
    total_inferences: int = 0
    avg_latency_us: float = 0.0
    loaded: bool = False


@dataclass
class MetricsSnapshot:
    """Snapshot of accelerator metrics."""
    gpu_util_percent: float = 0.0
    dla0_util_percent: float = 0.0
    dla1_util_percent: float = 0.0
    pva_util_percent: float = 0.0
    gpu_mem_total_mb: int = 0
    gpu_mem_used_mb: int = 0
    total_inferences: int = 0
    avg_latency_us: float = 0.0
    p99_latency_us: float = 0.0
    inferences_per_second: int = 0
    timestamp_us: int = 0


@dataclass
class InferenceResult:
    """Result of an inference request."""
    success: bool = False
    output_data: bytes = b""
    latency_us: int = 0
    error_message: str = ""


@dataclass
class HealthStatus:
    """Server health status."""
    status: int = 0  # 0=UNKNOWN, 1=SERVING, 2=NOT_SERVING
    version: str = ""
    uptime_us: int = 0
