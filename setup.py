#!/usr/bin/env python

import sys
from setuptools.command.test import test as TestCommand
from distutils.core import setup

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(name='Tlask',
      version='0.1',
      description='An async Telegram bot library',
      author='Jelle Besseling',
      author_email='jellebesseling@gmail.com',
      url='https://github.com/pingiun/tlask',
      packages=['tlask', 'tlask.middleware'],
      license='MIT',
      install_requires=['aiohttp>=0.21.0'],
      tests_require=['pytest>=2.9.0', 'pytest-asyncio>=0.4.0'],
      cmdclass={'test': PyTest},
     )