#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

try:
    from setuptools import setup
    setup  # workaround for pyflakes issue #13
except ImportError:
    from distutils.core import setup

# Hack to prevent stupid TypeError: 'NoneType' object is not callable error on
# exit of python setup.py test # in multiprocessing/util.py _exit_function when
# running python setup.py test (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
    multiprocessing
except ImportError:
    pass

# path prefix to build from
loc = os.path.abspath(os.path.dirname(__file__))


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


def read_file(*path_pieces):
    with open(os.path.join(loc, *path_pieces), 'r') as f:
        return f.read()


def get_version():
    path_parts = ('github_backup', '__init__.py')
    init_file = read_file(*path_parts)
    version_match = re.search(r'^__version__ = [\'"](.*)[\'"]$', init_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Could not find version string")


setup(
    name='github-backup',
    version=get_version(),
    author='Jose Diaz-Gonzalez',
    author_email='github-backup@josediazgonzalez.com',
    packages=['github_backup'],
    scripts=['bin/github-backup'],
    url='http://github.com/josegonzalez/python-github-backup',
    license=open('LICENSE.txt').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: System :: Archiving :: Backup',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description='backup a github user or organization',
    long_description=open_file('README.rst').read(),
    install_requires=open_file('requirements.txt').readlines(),
    zip_safe=True,
)
