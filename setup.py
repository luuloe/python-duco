#!/usr/bin/env python3
"""Python Duco setup script."""
import os
from setuptools import setup, find_packages
from duco.const import (__version__, PROJECT_PACKAGE_NAME,
                        PROJECT_LICENSE, PROJECT_URL,
                        PROJECT_EMAIL, PROJECT_DESCRIPTION,
                        PROJECT_CLASSIFIERS, GITHUB_URL,
                        PROJECT_AUTHOR)

HERE = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_URL = ('{}/archive/'
                '{}.zip'.format(GITHUB_URL, __version__))

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'pymodbus==1.3.2',
]

setup(
    name=PROJECT_PACKAGE_NAME,
    version=__version__,
    license=PROJECT_LICENSE,
    url=PROJECT_URL,
    download_url=DOWNLOAD_URL,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    description=PROJECT_DESCRIPTION,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=REQUIRES,
    test_suite='tests',
    keywords=['duco', 'ventilation'],
    classifiers=PROJECT_CLASSIFIERS,
    entry_points={
        'console_scripts': ['duco=duco.command_line:main'],
    }
)
