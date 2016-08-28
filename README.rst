=============
Crossbar HTTP
=============

.. image:: https://img.shields.io/pypi/v/crossbarhttp.svg
    :target: https://pypi.python.org/pypi/crossbarhttp

.. image:: https://img.shields.io/pypi/dm/crossbarhttp.svg
    :target: https://pypi.python.org/pypi/crossbarhttp

.. image:: https://img.shields.io/circleci/token/7e41f7fa67cadba9f0a3465cfb04fdeee4c31357/project/thehq/python-crossbarhttp/master.svg
    :target: https://circleci.com/gh/thehq/python-crossbarhttp/tree/master

.. image:: https://codecov.io/gh/thehq/python-crossbarhttp/branch/master/graph/badge.svg
    :target: https://codecov.io/github/thehq/python-crossbarhttp

.. image:: https://img.shields.io/pypi/l/crossbarhttp.svg
    :target: https://pypi.python.org/pypi/crossbarhttp

Module that provides methods for accessing Crossbar.io HTTP Bridge Services

Revision History
================

  - v0.1.2:
    - Added "ClientCallRuntimeError" exception for general errors
  - v0.1.1:
    - Added class defined Exceptions for specific events
    - Added key/secret handling
  - v0.1:
    - Initial version

Installation
============

    pip install crossbarhttp

Usage
=====

Call
----

To call a Crossbar HTTP bridge, do the following:

.. code-block:: python

    client = Client("http://127.0.0.1/call")
    result = client.call("com.example.add", 2, 3, offset=10)
    
This will call the following method:

.. code-block:: python

    def onJoin(self, details):
        
        def add_something(x, y, offset=0):
            print("Add was called")
            return x + y + offset

        self.register(add_something, "com.example.add")
        
Publish
-------

To publish to a Crossbar HTTP bridge, do the following:

.. code-block:: python

    client = Client("http://127.0.0.1/publish")
    result = client.publish("com.example.event", event="new event")
    
The receiving subscription would look like:

.. code-block:: python

    def onJoin(self, details):
        
        def subscribe_something(event=None, **kwargs):
            print("Publish was called with event %s" % event)

        self.subscribe(subscribe_something, "com.example.event") 

Key/Secret
----------

For bridge services that have a key and secret defined, simply include the key
and secret in the instantiation of the client.

.. code-block:: python

    client = Client("http://127.0.0.1/publish", key="key", secret="secret")

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

To contribute, fork the repo and submit a pull request.

Testing
=======

The test can be run by using `Docker Compose`_.  Connect to a Docker host and
type::

    %> docker-compose build
    %> docker-compose up

The Docker Compose file creates a generic router with an example service
connected to it and runs the tests.
    
The service ``crossbarhttp_test_`` will return a 0 value if the tests were
successful and non zero otherwise. To get the pass/fail results from a command
line, do the following:

.. code-block:: shell

    #!/usr/bin/env bash
    
    docker-compose build
    docker-compose up
    
    exit $(docker-compose ps -q | xargs docker inspect -f '{{ .Name }} exited with status {{ .State.ExitCode }}' | grep test_1 | cut -f5 -d ' ')

This is a little hacky (and hopefully Docker will fix it) but it will do the trick for now.

License
=======

`MIT License`_

.. _Docker Compose: https://docs.docker.com/compose/
.. _MIT License: https://opensource.org/licenses/MIT