import os
import unittest

import crossbarhttp
from crossbarhttp.compat import mock


class CrossbarHttpTests(unittest.TestCase):

    url = None

    @classmethod
    def setUpClass(cls):
        cls.url = os.getenv('ROUTER_URL', "http://localhost:8080")

    def test_call(self):
        client = crossbarhttp.Client(self.__class__.url + "/call")
        result = client.call("test.add", 2, 3, offset=10)
        self.assertEqual(result, 15)

    def test_publish(self):
        client = crossbarhttp.Client(self.__class__.url + "/publish")
        publish_id = client.publish("test.publish", 4, 7, event="new event")
        self.assertNotEqual(publish_id, None)

    def test_call_no_callee(self):
        client = crossbarhttp.Client(self.__class__.url + "/call")

        with self.assertRaises(crossbarhttp.ClientNoCalleeRegistered):
            client.call("test.does_not_exist", 2, 3, offset=10)

    def test_call_bad_url(self):
        client = crossbarhttp.Client(self.__class__.url + "/call_bad_url")

        with self.assertRaises(crossbarhttp.ClientBadUrl):
            client.call("test.add", 2, 3, offset=10)

    def test_publish_bad_url(self):
        client = crossbarhttp.Client(self.__class__.url + "/publish_bad_url")

        with self.assertRaises(crossbarhttp.ClientBadUrl):
            client.publish("test.publish", 4, 7, event="new event")

    def test_call_bad_host(self):
        client = crossbarhttp.Client("http://bad:8080/call")

        with self.assertRaises(crossbarhttp.ClientBadHost):
            client.call("test.add", 2, 3, offset=10)

    def test_publish_bad_host(self):
        client = crossbarhttp.Client("http://bad:8080/publish")

        with self.assertRaises(crossbarhttp.ClientBadHost):
            client.publish("test.publish", 4, 7, event="new event")

    def test_call_missing_signature_params(self):
        client = crossbarhttp.Client(self.__class__.url + "/call-signature")

        with self.assertRaises(crossbarhttp.ClientMissingParams):
            client.call("test.add", 2, 3, offset=10)

    def test_call_bad_signature(self):
        client = crossbarhttp.Client(self.__class__.url + "/call-signature",
                                     key="key", secret="bad secret")

        with self.assertRaises(crossbarhttp.ClientSignatureError):
            client.call("test.add", 2, 3, offset=10)

    def test_call_signature(self):
        client = crossbarhttp.Client(self.__class__.url + "/call-signature",
                                     key="key", secret="secret")
        result = client.call("test.add", 2, 3, offset=10)
        self.assertEqual(result, 15)

    def test_publish_missing_signature_params(self):
        client = crossbarhttp.Client(self.__class__.url + "/publish-signature")

        with self.assertRaises(crossbarhttp.ClientMissingParams):
            client.publish("test.publish", 4, 7, event="new event")

    def test_publish_bad_signature(self):
        client = crossbarhttp.Client(self.__class__.url + "/publish-signature",
                                     key="key", secret="bad secret")

        with self.assertRaises(crossbarhttp.ClientSignatureError):
            client.publish("test.publish", 4, 7, event="new event")

    def test_publish_signature(self):
        client = crossbarhttp.Client(self.__class__.url + "/publish-signature",
                                     key="key", secret="secret")
        publish_id = client.publish("test.publish", 4, 7, event="new event")
        self.assertNotEqual(publish_id, None)

    def test_verbose(self):
        client = crossbarhttp.Client(self.__class__.url + "/call-signature",
                                     key="key", secret="secret", verbose=True)
        result = client.call("test.add", 2, 3, offset=10)
        self.assertEqual(result, 15)

    def test_invalid_call_params(self):
        client = crossbarhttp.Client(self.__class__.url + "/call-signature",
                                     key="key", secret="secret")

        client._make_api_call = mock.MagicMock(return_value="{}")

        result = client.call("test.add", 2, 3, offset=10)
        self.assertEqual(result, None)

    def test_no_call_params(self):
        client = crossbarhttp.Client(self.__class__.url + "/call")

        with self.assertRaises(crossbarhttp.ClientMissingParams):
            client._make_api_call("POST", client.url)

    def test_call_exception(self):
        client = crossbarhttp.Client(self.__class__.url + "/call")
        with self.assertRaises(crossbarhttp.ClientCallRuntimeError):
            client.call("test.exception")


if __name__ == '__main__':
    unittest.main()
