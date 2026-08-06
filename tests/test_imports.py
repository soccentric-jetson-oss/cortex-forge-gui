import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestImports(unittest.TestCase):
    """Import verification tests for Cortex Forge GUI."""

    def test_grpc_import(self):
        """Verify gRPC module imports successfully."""
        import grpc
        self.assertIsNotNone(grpc)

    def test_protobuf_import(self):
        """Verify generated protobuf module imports successfully."""
        from src.client import cortex_forge_pb2
        self.assertIsNotNone(cortex_forge_pb2)


if __name__ == "__main__":
    unittest.main()
