import json
import os
import unittest

from crossbarhttp import (
    ClientBadUrl,
    ClientBadHost,
    ClientCallRuntimeError,
    ClientMissingParams,
    ClientNoCalleeRegistered,
    ClientSignatureError,
    Client
)
from crossbarhttp.compat import HTTPError, mock


class CrossbarHttpTests(unittest.TestCase):

    url = None

    @classmethod
    def setUpClass(cls):
        cls.url = os.getenv('ROUTER_URL', "http://localhost:8080")

    def test_call(self):
        client = Client(self.__class__.url + "/call")
        result = client.call("test.add", 2, 3, offset=10)
        self.assertEqual(result, 15)

    def test_publish(self):
        client = Client(self.__class__.url + "/publish")
        publish_id = client.publish("test.publish", 4, 7, event="new event")
        self.assertNotEqual(publish_id, None)

    def test_call_no_callee(self):
        client = Client(self.__class__.url + "/call")

        with self.assertRaises(ClientNoCalleeRegistered):
            client.call("test.does_not_exist", 2, 3, offset=10)

    def test_call_bad_url(self):
        client = Client(self.__class__.url + "/call_bad_url")

        with self.assertRaises(ClientBadUrl):
            client.call("test.add", 2, 3, offset=10)

    def test_publish_bad_url(self):
        client = Client(self.__class__.url + "/publish_bad_url")

        with self.assertRaises(ClientBadUrl):
            client.publish("test.publish", 4, 7, event="new event")

    def test_call_bad_host(self):
        client = Client("http://bad:8080/call")

        with self.assertRaises(ClientBadHost):
            client.call("test.add", 2, 3, offset=10)

    def test_publish_bad_host(self):
        client = Client("http://bad:8080/publish")

        with self.assertRaises(ClientBadHost):
            client.publish("test.publish", 4, 7, event="new event")

    def test_call_missing_signature_params(self):
        client = Client(self.__class__.url + "/call-signature")

        with self.assertRaises(ClientMissingParams):
            client.call("test.add", 2, 3, offset=10)

    def test_call_bad_signature(self):
        client = Client(self.__class__.url + "/call-signature",
                                     key="key", secret="bad secret")

        with self.assertRaises(ClientSignatureError):
            client.call("test.add", 2, 3, offset=10)

    def test_call_signature(self):
        client = Client(self.__class__.url + "/call-signature",
                                     key="key", secret="secret")
        result = client.call("test.add", 2, 3, offset=10)
        self.assertEqual(result, 15)

    def test_publish_missing_signature_params(self):
        client = Client(self.__class__.url + "/publish-signature")

        with self.assertRaises(ClientMissingParams):
            client.publish("test.publish", 4, 7, event="new event")

    def test_publish_bad_signature(self):
        client = Client(self.__class__.url + "/publish-signature",
                                     key="key", secret="bad secret")

        with self.assertRaises(ClientSignatureError):
            client.publish("test.publish", 4, 7, event="new event")

    def test_publish_signature(self):
        client = Client(self.__class__.url + "/publish-signature",
                                     key="key", secret="secret")
        publish_id = client.publish("test.publish", 4, 7, event="new event")
        self.assertNotEqual(publish_id, None)

    def test_invalid_call_params(self):
        client = Client(self.__class__.url + "/call-signature",
                                     key="key", secret="secret")

        client._make_api_call = mock.MagicMock(return_value="{}")

        result = client.call("test.add", 2, 3, offset=10)
        self.assertEqual(result, None)

    def test_no_call_params(self):
        client = Client(self.__class__.url + "/call")

        with self.assertRaises(ClientMissingParams):
            client._make_api_call("POST", client.url)

    def test_call_exception(self):
        client = Client(self.__class__.url + "/call")
        with self.assertRaises(ClientCallRuntimeError):
            client.call("test.exception")


class TestClient(unittest.TestCase):
    def setUp(self):
        self.crossbar_client = Client('http://localhost')

    def test_client_instantiation_wrong_url(self):
        """
        The client must be instantiated by passing an actually valid URL.
        """
        self.assertRaises(ClientBadUrl, Client, 'not a URL')

        self.assertRaises(ClientBadUrl, Client, None)

        self.assertRaises(ClientBadUrl, Client, 123456)

    def test_publish_topic_is_none(self):
        """
        The ``publish`` method ``topic`` parameter cannot be None.
        """
        self.assertRaises(AssertionError, self.crossbar_client.publish, None)

    @mock.patch('crossbarhttp.compat.urlopen')
    def test_publish_successful_response(self, urlopen_mock):
        """
        A successful response from the Crossbar.io node will make the method
        ``publish`` return the event ID.
        """
        # Mock Crossbar.io node successful POST request response.
        urlopen_mock().read.return_value = b'{"id":4354231544065071}'

        # Just send a useless 4 digits number as a message, 1234.
        self.assertEqual(
            self.crossbar_client.publish('http://localhost:8080', 1234),
            4354231544065071
        )

    @mock.patch('crossbarhttp.Client._make_api_call')
    def test_publish_request_failed_bad_host(self, api_call_mock):
        """
        Client must pass silently if the request to HTTP bridge fails due to a
        ``ClientBadHost`` exception and it is configured as ``silently=True``.
        """
        # Artificially raise the ``ClientBadHost`` exception.
        api_call_mock.side_effect = ClientBadHost

        crossbar_client = Client('http://localhost:8080', silently=True)
        self.assertEqual(
            crossbar_client.publish('http://localhost:8080', 1234),
            None
        )

    @mock.patch('crossbarhttp.Client._make_api_call')
    def test_publish_request_failed_bad_host_noisy(self, api_call_mock):
        """
        Client must raise the exception if the request to HTTP bridge fails due
        to a ``ClientBadHost`` exception.
        """
        # Artificially raise the ``ClientBadHost`` exception.
        api_call_mock.side_effect = ClientBadHost

        self.assertRaises(
            ClientBadHost,
            self.crossbar_client.publish,
            'http://localhost:8080', 1234
        )

    @mock.patch('crossbarhttp.Client._make_api_call')
    def test_publish_request_failed_bad_url(self, api_call_mock):
        """
        Client must pass silently if the request to HTTP bridge fails due to a
        ``ClientBadUrl`` exception and it is configured as ``silently=True``.
        """
        # Artificially raise the ``ClientBadUrl`` exception.
        api_call_mock.side_effect = ClientBadUrl

        crossbar_client = Client('http://localhost:8080', silently=True)
        self.assertEqual(
            crossbar_client.publish('http://localhost:8080', 1234),
            None
        )

    @mock.patch('crossbarhttp.Client._make_api_call')
    def test_publish_request_failed_bad_url_noisy(self, api_call_mock):
        """
        Client must raise the exception if the request to HTTP bridge fails due
        to a ``ClientBadUrl`` exception.
        """
        # Artificially raise the ``ClientBadUrl`` exception.
        api_call_mock.side_effect = ClientBadUrl

        self.assertRaises(
            ClientBadUrl,
            self.crossbar_client.publish,
            'http://localhost:8080', 1234
        )

    @mock.patch('crossbarhttp.Client._make_api_call')
    def test_publish_request_failed_missing_params(self, api_call_mock):
        """
        Client must pass silently if the request to HTTP bridge fails due to a
        ``ClientMissingParams`` exception and it is configured as
        ``silently=True``.
        """
        # Artificially raise the ``ClientMissingParams`` exception.
        api_call_mock.side_effect = ClientMissingParams

        crossbar_client = Client('http://localhost:8080', silently=True)
        self.assertEqual(
            crossbar_client.publish('http://localhost:8080', 1234),
            None
        )

    @mock.patch('crossbarhttp.Client._make_api_call')
    def test_publish_request_failed_missing_params_noisy(self, api_call_mock):
        """
        Client must raise the exception if the request to HTTP bridge fails due
        to a ``ClientMissingParams`` exception.
        """
        # Artificially raise the ``ClientMissingParams`` exception.
        api_call_mock.side_effect = ClientMissingParams

        self.assertRaises(
            ClientMissingParams,
            self.crossbar_client.publish,
            'http://localhost:8080', 1234
        )

    @mock.patch('crossbarhttp.Client._make_api_call')
    def test_publish_request_failed_signature_error(self, api_call_mock):
        """
        Client must pass silently if the request to HTTP bridge fails due to a
        ``ClientSignatureError`` exception and it is configured as
        ``silently=True``.
        """
        # Artificially raise the ``ClientSignatureError`` exception.
        api_call_mock.side_effect = ClientSignatureError

        crossbar_client = Client('http://localhost:8080', silently=True)
        self.assertEqual(
            crossbar_client.publish('http://localhost:8080', 1234),
            None
        )

    @mock.patch('crossbarhttp.Client._make_api_call')
    def test_publish_request_failed_signature_error_noisy(self, api_call_mock):
        """
        Client must raise the exception if the request to HTTP bridge fails due
        to a ``ClientSignatureError`` exception.
        """
        # Artificially raise the ``ClientSignatureError`` exception.
        api_call_mock.side_effect = ClientSignatureError

        self.assertRaises(
            ClientSignatureError,
            self.crossbar_client.publish,
            'http://localhost:8080', 1234
        )

    @mock.patch('crossbarhttp.compat.urlopen')
    def test_make_api_call_bad_request(self, urlopen_mock):
        """
        An HTTP 400 - Bad request error will raise a ``ClientMissingParams``
        exception.
        """
        # Mock Crossbar.io node response to be a 400 error.
        urlopen_mock().read.side_effect = HTTPError(
            url=self.crossbar_client.url,
            code=400,
            msg='Bad request',
            hdrs={},
            fp=None
        )

        self.assertRaises(
            ClientMissingParams,
            self.crossbar_client._make_api_call,
            'POST', self.crossbar_client.url, json_params={}
        )

    @mock.patch('crossbarhttp.compat.urlopen')
    def test_make_api_call_unauthorized(self, urlopen_mock):
        """
        An HTTP 401 - Unauthorized error will raise a ``ClientSignatureError``
        exception.
        """
        # Mock Crossbar.io node response to be a 401 error.
        urlopen_mock().read.side_effect = HTTPError(
            url=self.crossbar_client.url,
            code=401,
            msg='Unauthorized',
            hdrs={},
            fp=None
        )

        self.assertRaises(
            ClientSignatureError,
            self.crossbar_client._make_api_call,
            'POST', self.crossbar_client.url, json_params={}
        )

    @mock.patch('crossbarhttp.compat.urlopen')
    def test_make_api_call_bad_url(self, urlopen_mock):
        """
        An HTTP 4xx error which is not 400 or 401 will raise a ``ClientBadUrl``
        exception.
        """
        # Mock Crossbar.io node response to be a 418 error.
        urlopen_mock().read.side_effect = HTTPError(
            url=self.crossbar_client.url,
            code=418,
            msg='I am a teapot',
            hdrs={},
            fp=None
        )

        self.assertRaises(
            ClientBadUrl,
            self.crossbar_client._make_api_call,
            'POST', self.crossbar_client.url, json_params={}
        )

    @mock.patch('crossbarhttp.compat.urlopen')
    @mock.patch('crossbarhttp.compat.Request')
    def test_make_api_call_with_json_params(self, request_mock, urlopen_mock):
        """
        Tests ``Request.data`` composition when the method is called with some
        ``json_params``.
        """
        # Mock Crossbar.io node successful POST request response.
        urlopen_mock().read.return_value = b'{"id":4354231544065071}'

        params = {
            'topic': 'http://localhost:8080',
            'args': [1, 2, 3],
            'kwargs': {'key': 1234}
        }

        self.crossbar_client._make_api_call(
            'POST',
            self.crossbar_client.url,
            params
        )

        # `Request` object is instantiated with this `data`:
        encoded_params = json.dumps(params)
        request_mock.assert_called_with(
            self.crossbar_client.url,
            bytearray(encoded_params, 'utf-8'),
            {'Content-Type': 'application/json'}
        )

    @mock.patch('crossbarhttp.compat.urlopen')
    @mock.patch('crossbarhttp.compat.Request')
    def test_make_api_call_json_params_none(self, request_mock, urlopen_mock):
        """
        Tests ``Request`` instantiation when the method is called with
        ``json_params=None``.
        """
        # Mock Crossbar.io node successful POST request response.
        urlopen_mock().read.return_value = b'{"id":4354231544065071}'

        self.crossbar_client._make_api_call(
            'POST',
            self.crossbar_client.url,
            None
        )

        # `Request` object is instantiated with this `data`:
        request_mock.assert_called_with(self.crossbar_client.url, None, {})


if __name__ == '__main__':
    unittest.main()
