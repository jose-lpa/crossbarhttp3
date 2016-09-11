from __future__ import unicode_literals

import hashlib
import hmac
import json
import sys


# Compatibility workaround for `urllib`.
if sys.version_info >= (3,):
    # Python 3
    from http.client import HTTPException
    from urllib.parse import urlencode, urlparse
    from urllib.request import HTTPError, Request, URLError, urlopen

    def compute_hmac(body, key, secret, sequence, nonce, timestamp):
        """
        Performs the HMAC computation for signed requests, Python 3 compatible.
        """
        sequence = str(sequence)
        nonce = str(nonce)

        hm = hmac.new(bytes(secret, 'utf-8'), None, hashlib.sha256)
        hm.update(bytes(key, 'utf-8'))
        hm.update(bytes(timestamp, 'utf-8'))
        hm.update(bytes(sequence, 'utf-8'))
        hm.update(bytes(nonce, 'utf-8'))
        hm.update(bytes(body, 'utf-8'))

        return hm

    def send_request(request, timeout):
        """
        Performs a request to the Crossbar.io node, enabling the Python3
        timeout feature.

        :param request: The ``urllib.request.Request`` object to be sent.
        :param timeout: The timeout in seconds, passed from the ``Client``. If
        not specified, the global default timeout will be used.
        :return: The response data in a JSON payload.
        """
        if timeout is None:
            response = urlopen(request).read()
        else:
            response = urlopen(request, timeout=timeout).read()

        return json.loads(str(response, 'utf-8'))
else:
    # Python 2
    from builtins import bytes
    from httplib import HTTPException
    from urllib import urlencode
    from urllib2 import HTTPError, Request, URLError, urlopen
    from urlparse import urlparse

    def compute_hmac(body, key, secret, sequence, nonce, timestamp):
        """
        Performs the HMAC computation for signed requests, Python 2 compatible.
        """
        hm = hmac.new(secret, None, hashlib.sha256)
        hm.update(key)
        hm.update(timestamp)
        hm.update(str(sequence))
        hm.update(str(nonce))
        hm.update(body)

        return hm

    def send_request(request, timeout):
        """
        Performs a request to the Crossbar.io node, Python2 compatible.

        :param request: The `urllib.request.Request` object to perform the
        call.
        :param timeout: The timeout in seconds, passed from the ``Client``.
        :return: The response data.
        """
        if timeout is None:
            response = urlopen(request).read()
        else:
            response = urlopen(request, timeout=timeout).read()

        return json.loads(response)
