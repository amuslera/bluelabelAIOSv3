"""Basic test to ensure CI/CD pipeline works."""

def test_basic():
    """Basic test that always passes."""
    assert 1 == 1

def test_imports():
    """Test that we can import basic Python modules."""
    import sys
    import os
    assert sys.version_info >= (3, 9)
    assert os.path.exists(__file__)