#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'Jiang Bian <ji0ng.bi0n@gmail.com>'
__version__ = '0.0.1'

packages = [
    'tweeta'
]

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='tweeta',
    version=__version__,
    install_requires=['ftfy>=5.2.0', 'langid>=1.1.6'],
    author='Jiang Bian',
    author_email='ji0ng.bi0n@gmail.com',
    license=open('LICENSE').read(),
    url='https://github.com/bianjiang/tweeta/tree/master',
    keywords='twitter nlp',
    description='Various utilities for processing Twitter data (e.g., parsing, etc)',
    long_description=open('README.md').read() + '\n\n' +
        open('HISTORY.md').read(),
    include_package_data=True,
    packages=packages,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        #'Topic :: Communications :: Chat',
        'Topic :: Internet',
        #'Programming Language :: Python',
        #'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)