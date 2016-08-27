#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


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
    install_requires=[],
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
