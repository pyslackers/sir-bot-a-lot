#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import sys

from setuptools import setup, find_packages

from sirbot import DATA

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

def parse_reqs(req_path='./requirements.txt'):
    """Recursively parse requirements from nested pip files."""
    install_requires = []
    with codecs.open(req_path, 'r') as handle:
        # remove comments and empty lines
        lines = (line.strip() for line in handle
                 if line.strip() and not line.startswith('#'))

        for line in lines:
            # check for nested requirements files
            if line.startswith('-r'):
                # recursively call this function
                install_requires += parse_reqs(req_path=line[3:])

            else:
                # add the line as a new requirement
                install_requires.append(line)

    return install_requires

def parse_readme():
    """Parse contents of the README."""
    # Get the long description from the relevant file
    here = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(here, 'README.md')
    with codecs.open(readme_path, encoding='utf-8') as handle:
        long_description = handle.read()

    return long_description

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    long_description=parse_readme(),
    keywords='sirbot',
    packages=[
        'sirbot',
    ],
    package_dir={
        'sirbot': 'sirbot'
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and
    # allow pip to create the appropriate form of executable for the
    # target platform.
    entry_points={
        'console_scripts': [
            'sirbot=sirbot.cli:main'
        ]
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    include_package_data=True,
    install_requires=parse_reqs(),
    zip_safe=False,
    test_suite='tests',
    tests_require=test_requirements,
    # See: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
    ],
    author=DATA['author'],
    docker_name=DATA['docker_name'],
    docker_tag=DATA['docker_tag'],
    author_email=DATA['author_email'],
    copyright=DATA['copyright'],
    description=DATA['description'],
    license=DATA['license'],
    name=DATA['name'],
    url=DATA['url'],
    version=DATA['version'],
)
