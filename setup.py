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
    test_requirements = []
else:
    requirements = ['future']
    test_requirements = ['mock']


setup(
    name='crossbarhttp3',
    packages=['crossbarhttp'],
    version='1.1',
    description='Library for connecting to Crossbar.io HTTP Bridge Services.',
    author='José Luis Patiño Andrés',
    license='MIT',
    author_email='jose.lpa@gmail.com',
    url='https://github.com/jose-lpa/crossbarhttp3',
    keywords=['wamp', 'crossbar.io', 'websockets', 'http-bridge'],
    install_requires=requirements,
    test_suite='tests',
    tests_require=test_requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
)
