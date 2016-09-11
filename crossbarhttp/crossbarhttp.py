from __future__ import unicode_literals

import base64
import datetime
import json
import logging
from random import randint

from .compat import (
    compute_hmac, HTTPError, HTTPException, Request, send_request, urlencode,
    URLError, urlparse
)

logger = logging.getLogger('crossbarhttp')


class ClientBaseException(Exception):
    """
    Catch all Exception for this class.
    """
    pass


class ClientNoCalleeRegistered(ClientBaseException):
    """
    Exception thrown when no callee was registered.
    """
    pass


class ClientBadUrl(ClientBaseException):
    """
    Exception thrown when the URL is invalid.
    """
    pass


class ClientBadHost(ClientBaseException):
    """
    Exception thrown when the host name is invalid.
    """
    pass


class ClientMissingParams(ClientBaseException):
    """
    Exception thrown when the request is missing params.
    """
    pass


class ClientSignatureError(ClientBaseException):
    """
    Exception thrown when the signature check fails (if server has "key" and
    "secret" set).
    """
    pass


class ClientCallRuntimeError(ClientBaseException):
    """
    Exception thrown when a call generated an exception.
    """
    pass


class Client(object):

    def __init__(self, url, key=None, secret=None, timeout=None, silently=False):
        """
        Creates a client to connect to the HTTP bridge services.

        :param url: The URL to connect to to access the Crossbar.
        :param key: The key for the API calls.
        :param secret: The secret for the API calls.
        :param timeout: Time to wait for the connection, in seconds.
        :param silently: Whether the client should raise an exception or not if
        the request fails. Defaults to raise exceptions on request failure.
        """
        # URL sanity check.
        try:
            parsed = urlparse(url)
            assert parsed.scheme and parsed.netloc
        except (AssertionError, AttributeError):
            raise ClientBadUrl('Invalid Crossbar node URL')

        if key is None:
            key = ''
        if secret is None:
            secret = ''

        self.url = url
        self.key = key
        self.secret = secret
        self.sequence = 1
        self.timeout = timeout
        self.silently = silently

    def publish(self, topic, *args, **kwargs):
        """
        Publishes the request to the bridge service.

        :param topic: The topic to publish to.
        :param args: The arguments.
        :param kwargs: The key/word arguments.
        :return: The ID of the publish. In case the request failed, it returns
        ``None`` if ``self.silently`` is ``True``; otherwise it raises the
        exception.
        """
        assert topic is not None

        params = {
            "topic": topic,
            "args": args,
            "kwargs": kwargs
        }

        try:
            response = self._make_api_call("POST", self.url, json_params=params)
            return response["id"]
        except (
            ClientBadHost,
            ClientBadUrl,
            ClientMissingParams,
            ClientSignatureError,
            HTTPException
        ):
            logger.exception("Couldn't publish message: %r", params)
            if self.silently is True:
                return None
            else:
                raise

    def call(self, procedure, *args, **kwargs):
        """
        Calls a procedure from the bridge service.

        :param procedure: The procedure to call.
        :param args: The arguments.
        :param kwargs: The key/word arguments.
        :return: The response from calling the procedure.
        """
        assert procedure is not None

        params = {
            "procedure": procedure,
            "args": args,
            "kwargs": kwargs
        }

        response = self._make_api_call("POST", self.url, json_params=params)

        value = None
        if "args" in response and len(response["args"]) > 0:
            value = response["args"][0]

        if "error" in response:
            error = response["error"]
            if "wamp.error.no_such_procedure" in error:
                raise ClientNoCalleeRegistered(value)
            else:
                raise ClientCallRuntimeError(value)

        return value

    def _compute_signature(self, body):
        """
        Computes the signature.

        Described at:
        http://crossbar.io/docs/HTTP-Bridge-Publisher/#signed-requests

        Reference code is at:
        https://github.com/crossbario/crossbar/blob/master/crossbar/adapter/rest/common.py

        :return: (signature, nonce, timestamp)
        """
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        nonce = randint(0, 2 ** 53)

        hm = compute_hmac(
            body=body,
            key=self.key,
            secret=self.secret,
            sequence=self.sequence,
            nonce=nonce,
            timestamp=timestamp
        )
        signature = base64.urlsafe_b64encode(hm.digest())

        return signature, nonce, timestamp

    def _make_api_call(self, method, url, json_params=None):
        """
        Performs the REST API Call.

        :param method: HTTP Method
        :param url:  The URL
        :param json_params: The parameters intended to be JSON serialized
        :return: JSON response.
        """
        logger.debug('Request: %s %s', method, url)

        if json_params is not None:
            encoded_params = json.dumps(json_params)
            headers = {'Content-Type': 'application/json'}
            logger.debug('Params: %s', encoded_params)
            byte_encoded_params = bytearray(encoded_params, 'utf-8')
        else:
            encoded_params = None
            headers = {}
            byte_encoded_params = None

        if self.key and self.secret and encoded_params:
            signature, nonce, timestamp = self._compute_signature(encoded_params)
            params = urlencode({
                "timestamp": timestamp,
                "seq": str(self.sequence),
                "nonce": nonce,
                "signature": signature,
                "key": self.key
            })
            logger.debug('Signature Params: %s', params)

            url = '{0}?{1}'.format(url, params)

        self.sequence += 1

        try:
            request = Request(url, byte_encoded_params, headers)
            request.get_method = lambda: method
            response = send_request(request, self.timeout)
            logger.debug('Response: %s', response)
            return response

        except HTTPError as e:
            if e.code == 400:
                raise ClientMissingParams(str(e))
            elif e.code == 401:
                raise ClientSignatureError(str(e))
            else:
                raise ClientBadUrl(str(e))
        except URLError as e:
            raise ClientBadHost(str(e))
