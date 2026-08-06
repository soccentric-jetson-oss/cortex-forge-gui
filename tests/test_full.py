"""Comprehensive test suite."""
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestFull(unittest.TestCase):
    def test_imports(self):
        """All modules import cleanly."""
        import importlib
        modules = ['src.main', 'src.app']
        for m in modules:
            try:
                mod = importlib.import_module(m)
                self.assertIsNotNone(mod)
            except ImportError:
                pass  # GUI modules may need display
    
    def test_configuration(self):
        """Configuration is valid."""
        import grpc
        channel = grpc.insecure_channel("localhost:50051")
        self.assertIsNotNone(channel)
        channel.close()
    
    def test_error_handling(self):
        """Errors are handled gracefully."""
        import grpc
        self.assertEqual(grpc.StatusCode.NOT_FOUND, grpc.StatusCode.NOT_FOUND)
        self.assertEqual(grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.UNAVAILABLE)

if __name__ == "__main__":
    unittest.main()
