# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cortex Forge Contributors

"""
gRPC client for Cortex Forge Server.

Communicates with the Cortex Forge gRPC server for model management,
inference, and metrics monitoring.
"""

import grpc
import time
import threading
from typing import Optional, Callable
from concurrent import futures

# Import generated protobuf modules
# These are generated from proto/cortex_forge.proto
try:
    from src.client import cortex_forge_pb2
    from src.client import cortex_forge_pb2_grpc
except ImportError:
    # Fallback: generate on first import
    import os
    import sys
    from grpc_tools import protoc

    proto_dir = os.path.join(os.path.dirname(__file__), "..", "..", "proto")
    proto_file = os.path.join(proto_dir, "cortex_forge.proto")
    out_dir = os.path.dirname(__file__)

    if os.path.exists(proto_file):
        protoc.main([
            "grpc_tools.protoc",
            f"--proto_path={proto_dir}",
            f"--python_out={out_dir}",
            f"--grpc_python_out={out_dir}",
            proto_file
        ])
        from src.client import cortex_forge_pb2
        from src.client import cortex_forge_pb2_grpc


class GrpcClient:
    """gRPC client for Cortex Forge Server."""

    def __init__(self):
        self._channel: Optional[grpc.Channel] = None
        self._stub: Optional[object] = None
        self._connected = False
        self._lock = threading.Lock()

    def connect(self, host: str = "localhost", port: int = 50051) -> bool:
        """Connect to the gRPC server."""
        try:
            address = f"{host}:{port}"
            self._channel = grpc.insecure_channel(
                address,
                options=[
                    ("grpc.connect_timeout_ms", 2000),
                    ("grpc.keepalive_time_ms", 5000),
                ]
            )
            self._stub = cortex_forge_pb2_grpc.CortexForgeStub(self._channel)

            # Test connection with health check
            response = self._stub.HealthCheck(
                cortex_forge_pb2.HealthCheckRequest(),
                timeout=2
            )
            self._connected = response.status == cortex_forge_pb2.HealthCheckResponse.SERVING
            return self._connected
        except Exception as e:
            self._connected = False
            return False

    def disconnect(self):
        """Disconnect from the server."""
        with self._lock:
            if self._channel:
                self._channel.close()
            self._channel = None
            self._stub = None
            self._connected = False

    def is_connected(self) -> bool:
        """Check if connected to the server."""
        return self._connected

    # ── Model Management ──────────────────────────────────────────────────

    def load_model(self, model_path: str, model_name: str = "",
                   framework: str = "tensorrt",
                   accelerator: str = "auto") -> Optional[dict]:
        """Load a model on the server."""
        if not self._stub:
            return None
        try:
            request = cortex_forge_pb2.LoadModelRequest(
                model_path=model_path,
                model_name=model_name,
                framework=framework,
                accelerator=accelerator,
            )
            response = self._stub.LoadModel(request, timeout=10)
            return {
                "model_id": response.model_id,
                "model_name": response.model_name,
                "success": response.success,
                "error": response.error_message,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def unload_model(self, model_id: str) -> bool:
        """Unload a model."""
        if not self._stub:
            return False
        try:
            request = cortex_forge_pb2.UnloadModelRequest(model_id=model_id)
            response = self._stub.UnloadModel(request, timeout=5)
            return response.success
        except Exception:
            return False

    def list_models(self) -> list:
        """List all loaded models."""
        if not self._stub:
            return []
        try:
            request = cortex_forge_pb2.ListModelsRequest()
            response = self._stub.ListModels(request, timeout=5)
            models = []
            for model in response.models:
                models.append({
                    "model_id": model.model_id,
                    "model_name": model.model_name,
                    "framework": model.framework,
                    "batch_size": model.batch_size,
                    "accelerator": model.accelerator,
                    "total_inferences": model.total_inferences,
                    "avg_latency_us": model.avg_latency_us,
                    "loaded": model.loaded,
                })
            return models
        except Exception:
            return []

    # ── Inference ─────────────────────────────────────────────────────────

    def infer(self, model_id: str, input_data: bytes = b"") -> Optional[dict]:
        """Run inference on a model."""
        if not self._stub:
            return None
        try:
            request = cortex_forge_pb2.InferRequest(
                model_id=model_id,
                input_data=input_data,
            )
            response = self._stub.Infer(request, timeout=30)
            return {
                "success": response.success,
                "output_data": response.output_data,
                "latency_us": response.latency_us,
                "error": response.error_message,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ── Metrics ───────────────────────────────────────────────────────────

    def get_metrics(self) -> Optional[dict]:
        """Get current accelerator metrics."""
        if not self._stub:
            return None
        try:
            request = cortex_forge_pb2.GetMetricsRequest()
            response = self._stub.GetMetrics(request, timeout=5)
            m = response.current
            return {
                "gpu_util_percent": m.gpu_util_percent,
                "dla0_util_percent": m.dla0_util_percent,
                "dla1_util_percent": m.dla1_util_percent,
                "pva_util_percent": m.pva_util_percent,
                "gpu_mem_total_mb": m.gpu_mem_total_mb,
                "gpu_mem_used_mb": m.gpu_mem_used_mb,
                "total_inferences": m.total_inferences,
                "avg_latency_us": m.avg_latency_us,
                "p99_latency_us": m.p99_latency_us,
                "inferences_per_second": m.inferences_per_second,
            }
        except Exception:
            return None

    def watch_metrics(self, callback: Callable, interval_ms: int = 1000):
        """Stream metrics from the server."""
        if not self._stub:
            return

        def _stream():
            try:
                request = cortex_forge_pb2.GetMetricsRequest()
                for snapshot in self._stub.WatchMetrics(request):
                    callback({
                        "gpu_util_percent": snapshot.gpu_util_percent,
                        "dla0_util_percent": snapshot.dla0_util_percent,
                        "dla1_util_percent": snapshot.dla1_util_percent,
                        "pva_util_percent": snapshot.pva_util_percent,
                        "gpu_mem_total_mb": snapshot.gpu_mem_total_mb,
                        "gpu_mem_used_mb": snapshot.gpu_mem_used_mb,
                        "total_inferences": snapshot.total_inferences,
                        "avg_latency_us": snapshot.avg_latency_us,
                        "p99_latency_us": snapshot.p99_latency_us,
                        "inferences_per_second": snapshot.inferences_per_second,
                        "timestamp_us": snapshot.timestamp_us,
                    })
            except Exception:
                pass

        thread = threading.Thread(target=_stream, daemon=True)
        thread.start()

    # ── Health ────────────────────────────────────────────────────────────

    def health_check(self) -> Optional[dict]:
        """Check server health."""
        if not self._stub:
            return None
        try:
            request = cortex_forge_pb2.HealthCheckRequest()
            response = self._stub.HealthCheck(request, timeout=2)
            return {
                "status": response.status,
                "version": response.version,
                "uptime_us": response.uptime_us,
            }
        except Exception:
            return None
