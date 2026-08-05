# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cortex Forge Contributors

"""
Tests for the gRPC client.
"""

import unittest
from unittest.mock import MagicMock, patch
from src.client.grpc_client import GrpcClient


class TestGrpcClient(unittest.TestCase):
    """Test the gRPC client."""

    def setUp(self):
        self.client = GrpcClient()

    def test_initial_state(self):
        """Client starts disconnected."""
        self.assertFalse(self.client.is_connected())

    def test_connect_failure(self):
        """Connect to non-existent server returns False."""
        result = self.client.connect("localhost", 9999)
        self.assertFalse(result)

    def test_disconnect(self):
        """Disconnect doesn't raise."""
        self.client.disconnect()
        self.assertFalse(self.client.is_connected())

    def test_list_models_when_disconnected(self):
        """List models returns empty list when disconnected."""
        models = self.client.list_models()
        self.assertEqual(models, [])

    def test_get_metrics_when_disconnected(self):
        """Get metrics returns None when disconnected."""
        metrics = self.client.get_metrics()
        self.assertIsNone(metrics)

    def test_health_check_when_disconnected(self):
        """Health check returns None when disconnected."""
        result = self.client.health_check()
        self.assertIsNone(result)

    def test_infer_when_disconnected(self):
        """Infer returns None when disconnected."""
        result = self.client.infer("test-model")
        self.assertIsNone(result)

    def test_load_model_when_disconnected(self):
        """Load model returns None when disconnected."""
        result = self.client.load_model("/test/path")
        self.assertIsNone(result)

    def test_unload_model_when_disconnected(self):
        """Unload model returns False when disconnected."""
        result = self.client.unload_model("test-model")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
