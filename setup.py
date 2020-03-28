#!/usr/bin/env python

import os
import pip
import sys
import re
import uuid
import pkg_resources
from setuptools import setup, find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'Jiang Bian <ji0ng.bi0n@gmail.com>'

VERSIONFILE = "tweeta/__init__.py"
ver_file = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, ver_file, re.M)

if mo:
    version = mo.group(1)
    __version__ = version
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


def _parse_requirements(filepath):
    pip_version = list(map(int, pkg_resources.get_distribution('pip').version.split('.')[:2]))
    if pip_version >= [10, 0]:
        #from pip._internal.download import PipSession
        from pip._internal.req import parse_requirements
        raw = parse_requirements(filepath, session='hack')
    elif pip_version >= [6, 0]:
        from pip.download import PipSession
        from pip.req import parse_requirements
        raw = parse_requirements(filepath, session=PipSession())
    else:
        from pip.req import parse_requirements
        raw = parse_requirements(filepath)

    return [str(i.req) for i in raw]
    
reqs = _parse_requirements('requirements.txt')
#reqs = [str(req.req) for req in install_reqs]

packages = [
    'tweeta'
]

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='tweeta',
    version=__version__,
    install_requires=reqs,
    author='Jiang Bian',
    author_email='ji0ng.bi0n@gmail.com',
    license=open('LICENSE').read(),
    url='https://github.com/bianjiang/tweeta',
    keywords='twitter nlp',
    description='A collection utitlity funtions to process Twittwer data (e.g., turn raw json into python object with safe checks)',
    long_description=open('README.md').read() + '\n\n' +
        open('HISTORY.md').read(),
    include_package_data=True,
    packages=packages,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
