# coding: utf-8
"""Constants used by duco."""
MAJOR_VERSION = 0
MINOR_VERSION = 1
PATCH_VERSION = '0.dev0'
__short_version__ = '{}.{}'.format(MAJOR_VERSION, MINOR_VERSION)
__version__ = '{}.{}'.format(__short_version__, PATCH_VERSION)
REQUIRED_PYTHON_VER = (3, 4, 2)
REQUIRED_PYTHON_VER_WIN = (3, 4, 2)
CONSTRAINT_FILE = 'package_constraints.txt'

PROJECT_NAME = 'Python Duco'
PROJECT_PACKAGE_NAME = 'python-duco'
PROJECT_LICENSE = 'Apache License 2.0'
PROJECT_AUTHOR = 'Luuk Loeffen'
PROJECT_COPYRIGHT = ' 2017, {}'.format(PROJECT_AUTHOR)
PROJECT_EMAIL = 'luukloeffen@hotmail.com'
PROJECT_DESCRIPTION = ('Open-source Python 3 library that allows '
                       'communication to the Duco Ventilation System.')
PROJECT_CLASSIFIERS = [
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.4',
    'Topic :: Home Automation',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

PROJECT_GITHUB_USERNAME = 'luuloe'
PROJECT_GITHUB_REPOSITORY = 'python-duco'

PYPI_URL = 'https://pypi.python.org/pypi/{}'.format(PROJECT_PACKAGE_NAME)
GITHUB_PATH = '{}/{}'.format(PROJECT_GITHUB_USERNAME,
                             PROJECT_GITHUB_REPOSITORY)
GITHUB_URL = 'https://github.com/{}'.format(GITHUB_PATH)

PROJECT_URL = GITHUB_URL

# duco module types
DUCO_MODULE_TYPE_MASTER = 10
DUCO_MODULE_TYPE_VALVE_SENSORLESS = 11
DUCO_MODULE_TYPE_VALVE_CO2 = 12
DUCO_MODULE_TYPE_VALVE_RH = 13
DUCO_MODULE_TYPE_USER_CONTROLLER = 14
DUCO_MODULE_TYPE_ROOM_SENSOR_CO2 = 15
DUCO_MODULE_TYPE_ROOM_SENSOR_RH = 16
DUCO_MODULE_TYPE_CTRL_WINDOW_VENT = 17
DUCO_MODULE_TYPE_ROOM_SWITCH = 18
DUCO_MODULE_TYPE_ACTUATOR_PRINT = 19

#
DUCO_MODULE_MASTER_DEFAULT_ADDRESS = 1
