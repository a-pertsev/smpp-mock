# coding=utf-8

import sys
from setuptools.command.test import test as TestCommand
from setuptools import setup


def get_version():
    return '0.01'


class PyTest(TestCommand):
    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='smpp_server_mock',
    version=get_version(),
    url='http://github.com/hhru/smpp-server-mock/',
    tests_require=['pytest'],
    install_requires=[
        'tornado>=4.0.0',
        'SQLAlchemy>=1.0.0',
    ],
    cmdclass={'test': PyTest},
    description='Simple smpp server mock',
    packages=['smpp_server_mock'],
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    extras_require={
        'testing': ['pytest'],
    }
)
