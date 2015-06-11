#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Ichabod',
    version='0.1',
    description='Python client for HTTP communication with Ichabod.',
    author='Eric Heydenberk, Dave Berton',
    author_email='eheydenberk@monetate.com, dberton@monetate.com',
    url='https://www.icahbod.org/',
    requires=['requests'],
    packages=['ichabod']
)
