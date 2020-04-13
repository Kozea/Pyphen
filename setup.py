#!/usr/bin/env python

import os.path
from setuptools import setup

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
    'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Linguistic',
]

setup(
    name='Pyphen',
    version='0.9.5',
    provides=['pyphen'],
    packages=['pyphen'],
    package_data={'pyphen': [os.path.join(
        os.path.dirname(__file__), 'dictionaries', '*.dic')]},
    include_package_data=True,
    author='Guillaume Ayoub',
    author_email='guillaume.ayoub@kozea.fr',
    url='https://github.com/Kozea/Pyphen',
    description='Pure Python module to hyphenate text',
    zip_safe=False,
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README')).read(),
    classifiers=classifiers,
)
