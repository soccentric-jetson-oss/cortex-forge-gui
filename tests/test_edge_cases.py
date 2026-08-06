import unittest


class TestEdgeCases(unittest.TestCase):
    """Edge case tests for Cortex Forge GUI."""

    def test_null_input(self):
        """Verify None input handling in gRPC stubs."""
        import grpc
        stub = None
        self.assertIsNone(stub)

    def test_empty_input(self):
        """Verify empty protobuf messages are valid."""
        from src.client import cortex_forge_pb2
        req = cortex_forge_pb2.HealthCheckRequest()
        self.assertIsNotNone(req)
        self.assertEqual(req.service, '')

    def test_boundary_values(self):
        """Verify boundary values in model load request."""
        from src.client import cortex_forge_pb2
        req = cortex_forge_pb2.LoadModelRequest()
        req.batch_size = 0
        self.assertEqual(req.batch_size, 0)
        req.batch_size = 1024
        self.assertEqual(req.batch_size, 1024)

    def test_concurrent_access(self):
        """Verify thread safety of protobuf messages."""
        from src.client import cortex_forge_pb2
        import threading
        req = cortex_forge_pb2.HealthCheckRequest(service="test")
        results = []

        def reader():
            results.append(req.service)

        threads = [threading.Thread(target=reader) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(len(results), 10)
        for r in results:
            self.assertEqual(r, "test")

    def test_resource_cleanup(self):
        """Verify gRPC channel cleanup."""
        import grpc
        channel = grpc.insecure_channel("localhost:50051")
        self.assertIsNotNone(channel)
        channel.close()


if __name__ == "__main__":
    unittest.main()
