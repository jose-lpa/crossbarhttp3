from __future__ import unicode_literals

import json
import sys

# Mock facility for unit testing.
try:
    # Python 3
    import unittest.mock as mock
except ImportError:
    # Python 2
    import mock


# Compatibility workaround for `urllib`.
if sys.version_info >= (3,):
    # Python 3
    from http.client import HTTPException
    from urllib.parse import urlencode, urlparse
    from urllib.request import HTTPError, Request, URLError, urlopen

    def send_request(request, timeout):
        """
        Performs a request to the Crossbar.io node, enabling the Python3
        timeout feature.

        :param request: The ``urllib.request.Request`` object to be sent.
        :param timeout: The timeout in seconds, passed from the ``Client``.
        :return: The response data in a JSON payload.
        """
        response = urlopen(request, timeout=timeout).read()

        return json.loads(str(response, 'utf-8'))
else:
    # Python 2
    from httplib import HTTPException
    from urllib import urlencode
    from urllib2 import HTTPError, Request, URLError, urlopen
    from urlparse import urlparse

    def send_request(request, timeout):
        """
        Performs a request to the Crossbar.io node, Python2 compatible.

        :param request: The `urllib.request.Request` object to perform the call.
        :param timeout: The timeout in seconds, passed from the ``Client``. It's
        here only for compatibility, not really used in this function version.
        :return: The response data.
        """
        response = urlopen(request).read()

        return json.loads(response)
