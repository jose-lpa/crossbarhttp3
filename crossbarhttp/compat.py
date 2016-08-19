import sys

# Mock facility for unit testing.
try:
    # Python 3
    import unittest.mock as mock
except ImportError:
    # Python 2
    import mock


# Compatibility workaround for `urllib`.
if sys.version_info >=(3,):
    # Python 3
    from urllib.parse import urlencode
    from urllib.request import HTTPError, Request, URLError, urlopen
else:
    from urllib import urlencode
    from urllib2 import HTTPError, Request, URLError, urlopen
