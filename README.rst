===============
Crossbar HTTP 3
===============

.. image:: https://travis-ci.org/jose-lpa/crossbarhttp3.svg?branch=master
    :target: https://travis-ci.org/jose-lpa/crossbarhttp3

.. image:: https://codecov.io/gh/jose-lpa/crossbarhttp3/branch/master/graph/badge.svg
    :target: https://codecov.io/github/jose-lpa/crossbarhttp3

.. image:: https://img.shields.io/pypi/v/crossbarhttp3.svg
    :target: https://pypi.python.org/pypi/crossbarhttp3

.. image:: https://img.shields.io/pypi/l/crossbarhttp3.svg
    :target: https://pypi.python.org/pypi/crossbarhttp3

Module that provides methods for accessing Crossbar.io HTTP Bridge Services

Fork of the original package by `Eric Chapman at The HQ`_, now supporting 
Python 2.6, 2.7 and 3+ versions.


Installation
============

Install Crossbar HTTP 3 with pip::

    pip install crossbarhttp3


Basic usage
===========

Call
----

To call a Crossbar HTTP bridge, do the following:

.. code-block:: python

    from crossbarhttp import Client

    client = Client('http://127.0.0.1/call')
    result = client.call('com.example.add', 2, 3, offset=10)
    
This will call the following ``add_something`` method of an `ApplicationSession object`_:

.. code-block:: python

    from autobahn.twisted.wamp import ApplicationSession
    from twisted.internet.defer import inlineCallbacks


    class MyComponent(ApplicationSession):
        @inlineCallbacks
        def onJoin(self, details):

            def add_something(x, y, offset=0):
                print('Add was called')
                return x + y + offset

            yield self.register(add_something, 'com.example.add')
        
Publish
-------

To publish to a Crossbar HTTP bridge, do the following:

.. code-block:: python

    from crossbarhttp import Client

    client = Client('http://127.0.0.1/publish')
    result = client.publish('com.example.event', event='new event')
    
The receiving subscription implemented in an ``ApplicationSession`` class would
look like this:

.. code-block:: python

    from autobahn.twisted.wamp import ApplicationSession
    from twisted.internet.defer import inlineCallbacks


    class MyComponent(ApplicationSession):
        @inlineCallbacks
        def onJoin(self, details):

            def subscribe_something(event=None, **kwargs):
                print('Publish was called with event %s' % event)

            yield self.subscribe(subscribe_something, 'com.example.event')

Key/Secret
----------

For bridge services that have a key and secret defined, simply include the key
and secret in the instantiation of the client.

.. code-block:: python

    from crossbarhttp import Client

    client = Client('http://127.0.0.1/publish', key='key', secret='secret')

Additional options
------------------

There are two more options available in the client instantiation:

- ``timeout``: Lets you specify a number of seconds from which an idle request to the Crossbar.io node will be dismissed (timed out). Defaults to ``None``, meaning that the global default timeout setting will be used.
- ``silently``: If set to ``True``, any failed request to the Crossbar.io node will be returned by the client as ``None``, **without raising any exception**. Defaults to ``False``, meaning that all failures will raise their correspondent exceptions.

Exceptions
----------

The library will throw the following exceptions.  Note that all exceptions
subclass from ``ClientBaseException`` so you can just catch that if you don't
want the granularity.

- ``ClientBadUrl`` - The specified URL is not a HTTP bridge service
- ``ClientBadHost`` - The specified host name is rejecting the connection
- ``ClientMissingParams`` - The call was missing parameters
- ``ClientSignatureError`` - The signature did not match
- ``ClientNoCalleeRegistered`` - Callee was not registered on the router for the specified procedure
- ``ClientCallRuntimeError`` - Procedure triggered an exception

Contributing
============

All bug-fixes or improvements to the library are welcome.

To contribute, fork the repo and submit a pull request to the ``develop``
branch. Please, try to follow this basic coding rules:

- Always include some unit tests for the new code you write or the bugs you fix. Or, update the existent unit tests if necessary.
- Stick to `PEP-8`_ styling.

Testing
-------

In order to test Crossbar HTTP 3 properly you must have a Crossbar.io node in
HTTP Bridge mode running in localhost port 8001. You can do that by yourself if
you need it, but otherwise there is a `Docker image`_ already prepared, so you
don't have to bother with this.

To use that image and raise a Docker container with everything working, make
sure you have `Docker installed`_ and execute this command::

    docker run -t -p 8001:8001 --name crossbar-bridge joselpa/crossbar-http-bridge:0.2

Then you can run the unit tests in the regular way::

    python setup.py test

License
=======

Released under `MIT License`_.

.. _Eric Chapman at The HQ: https://github.com/thehq/python-crossbarhttp
.. _ApplicationSession object: http://autobahn.ws/python/wamp/programming.html#creating-components
.. _PEP-8: https://www.python.org/dev/peps/pep-0008/
.. _Docker image: https://hub.docker.com/r/joselpa/crossbar-http-bridge/
.. _Docker installed: https://docs.docker.com/
.. _MIT License: https://opensource.org/licenses/MIT
