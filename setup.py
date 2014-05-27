#!/usr/bin/env python

from os.path import exists
try:
    # Use setup() from setuptools(/distribute) if available
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='conttest',
      version='0.0.8',
      author='John Jacobsen',
      author_email='john@mail.npxdesigns.com',
      packages=['conttest'],
      scripts=[],
      url='https://github.com/eigenhombre/continuous-testing-helper',
      license='MIT',
      description='Simple continuous testing tool',
      long_description=open('README.md').read() if exists("README.md") else "",
      entry_points=dict(console_scripts = ['conttest=conttest.conttest:main']),
      install_requires=[])
