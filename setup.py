#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from pathlib import Path
import sys

from setuptools import setup, convert_path


if sys.version_info < (3, 5):
    raise RuntimeError('SirBot requires Python 3.5+')


def load_package_meta():
    meta_path = convert_path('./sirbot/core/__meta__.py')
    meta_ns = {}
    with open(meta_path) as f:
        exec(f.read(), meta_ns)
    return meta_ns['DATA']


PKG_META = load_package_meta()


def parse_reqs(req_path='./requirements/requirements.txt'):
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
    readme_file = str(Path(__file__).parent / 'README.rst')
    with codecs.open(readme_file, encoding='utf-8') as handle:
        long_description = handle.read()

    return long_description


setup(
    long_description=parse_readme(),
    keywords=[
        'sirbot',
        'chatbot',
        'bot',
        'slack',
    ],
    packages=[
        'sirbot',
        'sirbot.core',
        'sirbot.utils',
        'sirbot.cli',
    ],
    package_dir={
        'sirbot': 'sirbot',
        'sirbot.core': 'sirbot/core',
        'sirbot.utils': 'sirbot/utils',
        'sirbot.cli': 'sirbot/cli',
    },
    package_data={
        'sirbot.core': ['config.yml'],
        'sirbot.cli': ['sirbot.yml.mako', 'plugin.py.mako']
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and
    # allow pip to create the appropriate form of executable for the
    # target platform.
    # entry_points={
    #     'console_scripts': [
    #         'sirbot=sirbot.cli:main'
    #     ]
    # },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    entry_points={
        'console_scripts': [
            'sirbot=sirbot.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=parse_reqs('./requirements/requirements.txt'),
    python_requires='~=3.5',
    zip_safe=False,
    tests_require=[
        'pytest-runner',
        'pytest-cov',
        'pytest-aiohttp',
        'pytest',
    ],
    extras_require={
        'dev': parse_reqs('./requirements/requirements_dev.txt')
    },
    # See: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
    ],
    author=PKG_META['author'],
    # docker_name=PKG_META['docker_name'],
    # docker_tag=PKG_META['docker_tag'],
    author_email=PKG_META['author_email'],
    # copyright=PKG_META['copyright'],
    description=PKG_META['description'],
    license=PKG_META['license'],
    name=PKG_META['name'],
    url=PKG_META['url'],
    version=PKG_META['version'],
    maintainer="pythondev slack community",
    maintainer_email=PKG_META['author_email']
)
