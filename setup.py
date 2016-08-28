#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# Define requirements per Python version.
if sys.version_info >= (3,):
    requirements = []
else:
    requirements = ['future']


setup(
    name='crossbarhttp',
    packages=['crossbarhttp'],
    version='0.1.2',
    description='Library for connecting to Crossbar.io HTTP Bridge Services.',
    author='Eric Chapman',
    license='MIT',
    author_email='eric@thehq.io',
    url='https://github.com/thehq/python-crossbarhttp',
    keywords=['wamp', 'crossbar', 'websockets'],
    install_requires=requirements,
    test_suite='tests',
    tests_require=[
        'autobahn',
        'twisted'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
)
