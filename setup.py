#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

from github_backup import __version__


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


setup(
    name='github-backup',
    version=__version__,
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description='backup a github user or organization',
    long_description=open_file('README.rst').read(),
    install_requires=open_file('requirements.txt').readlines(),
    zip_safe=True,
)
