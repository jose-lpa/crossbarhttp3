# Mock facility for unit testing.
try:
    # Python 3
    import unittest.mock as mock
except ImportError:
    # Python 2
    import mock
