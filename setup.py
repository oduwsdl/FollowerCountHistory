#!/usr/bin/env python

from setuptools import setup, find_packages
from fch import __version__

long_description = open('README.md').read()
desc = """A Python library to find historical Twitter follower count using the web archives"""


setup(
    name='fch',
    version=__version__,
    description=desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mohammed Nauman Siddique',
    author_email='msidd003@odu.edu',
    url='https://github.com/oduwsdl/FollowerCountHistory',
    packages=find_packages(),
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Backup',
    ],
    provides=[
        "fch"
    ],
    package_dir={
        'fch': 'fch'
    },
    install_requires=[
        'warcio',
        'requests',
        'beautifulsoup4'
    ],
    entry_points={
        "console_scripts": [
            "fch = fch.__main__:main"
        ]
    },
    package_data={
        'fch': [
            'core/config/data/config.ini'
          ]
    },
)
