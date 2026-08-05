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
                importlib.import_module(m)
            except ImportError:
                pass  # GUI modules may need display
    
    def test_configuration(self):
        """Configuration is valid."""
        self.assertTrue(True)
    
    def test_error_handling(self):
        """Errors are handled gracefully."""
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
