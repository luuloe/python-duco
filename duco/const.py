# coding: utf-8
"""Constants used by duco."""
MAJOR_VERSION = 0
MINOR_VERSION = 2
PATCH_VERSION = '0'
__short_version__ = '{}.{}'.format(MAJOR_VERSION, MINOR_VERSION)
__version__ = '{}.{}'.format(__short_version__, PATCH_VERSION)
REQUIRED_PYTHON_VER = (3, 6, 7)
REQUIRED_PYTHON_VER_WIN = (3, 6, 7)
CONSTRAINT_FILE = 'package_constraints.txt'

PROJECT_NAME = 'Python Duco'
PROJECT_PACKAGE_NAME = 'python-duco'
PROJECT_LICENSE = 'MIT License'
PROJECT_AUTHOR = 'Luuk Loeffen'
PROJECT_COPYRIGHT = ' 2020, {}'.format(PROJECT_AUTHOR)
PROJECT_EMAIL = 'luukloeffen@hotmail.com'
PROJECT_DESCRIPTION = ('Open-source Python 3 library that allows '
                       'communication to the Duco Ventilation System.')
PROJECT_CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.6',
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

# parameters:
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
DUCO_MODBUS_METHOD = 'rtu'
DUCO_MODBUS_BAUD_RATE = 9600
DUCO_MODBUS_BYTE_SIZE = 8
DUCO_MODBUS_STOP_BITS = 1
DUCO_MODBUS_PARITY = 'N'
DUCO_MODBUS_MASTER_DEFAULT_UNIT_ID = 1

# Python enum do not support value of 0, therefore incr register with offset
DUCO_ZONE_STATUS_OFFSET = 1
# duco zone status
DUCO_ZONE_STATUS_AUTO = 0+DUCO_ZONE_STATUS_OFFSET
DUCO_ZONE_STATUS_HIGH_10MIN = 1+DUCO_ZONE_STATUS_OFFSET
DUCO_ZONE_STATUS_HIGH_20MIN = 2+DUCO_ZONE_STATUS_OFFSET
DUCO_ZONE_STATUS_HIGH_30MIN = 3+DUCO_ZONE_STATUS_OFFSET
DUCO_ZONE_STATUS_MANUAL_LOW = 4+DUCO_ZONE_STATUS_OFFSET
DUCO_ZONE_STATUS_MANUAL_MEDIUM = 5+DUCO_ZONE_STATUS_OFFSET
DUCO_ZONE_STATUS_MANUAL_HIGH = 6+DUCO_ZONE_STATUS_OFFSET
DUCO_ZONE_STATUS_AWAY = 7+DUCO_ZONE_STATUS_OFFSET
DUCO_ZONE_STATUS_ERROR = 99+DUCO_ZONE_STATUS_OFFSET

# addressing
DUCO_REG_ADDR_NODE_ID_OFFSET = 10

DUCO_REG_ADDR_INPUT_MODULE_TYPE = 0
DUCO_REG_ADDR_INPUT_STATUS = 1
DUCO_REG_ADDR_INPUT_FAN_ACTUAL = 2
DUCO_REG_ADDR_INPUT_TEMPERATURE = 3
DUCO_REG_ADDR_INPUT_CO2_ACTUAL = 4
DUCO_REG_ADDR_INPUT_RH_ACTUAL = 5
DUCO_REG_ADDR_INPUT_GROUP = 9

DUCO_REG_ADDR_HOLD_FAN_SETPOINT = 0
DUCO_REG_ADDR_HOLD_CO2_SETPOINT = 1
DUCO_REG_ADDR_HOLD_RH_SETPOINT = 2
DUCO_REG_ADDR_HOLD_RH_DELTA = 3
DUCO_REG_ADDR_HOLD_FLOW = 4
DUCO_REG_ADDR_HOLD_BUTTON_1 = 4
DUCO_REG_ADDR_HOLD_AUTOMIN = 5
DUCO_REG_ADDR_HOLD_BUTTON_2 = 5
DUCO_REG_ADDR_HOLD_AUTOMAX = 6
DUCO_REG_ADDR_HOLD_BUTTON_3 = 6
DUCO_REG_ADDR_HOLD_MANUAL_TIME = 7
DUCO_REG_ADDR_HOLD_ACTION = 9

# input register
DUCO_TEMPERATURE_SCALE_FACTOR = 0.1
DUCO_TEMPERATURE_PRECISION = 1
DUCO_RH_SCALE_FACTOR = 0.01
DUCO_RH_PRECISION = 2

# holding register limits
# duco fan setpoint
DUCO_FAN_SETPOINT_OVERRIDE_OFF = -1
DUCO_FAN_SETPOINT_MIN = 0
DUCO_FAN_SETPOINT_RES = 5
DUCO_FAN_SETPOINT_MAX = 100
DUCO_FAN_SETPOINT_DEFAULT = DUCO_FAN_SETPOINT_OVERRIDE_OFF
# duco co2 setpoint
DUCO_CO2_SETPOINT_MIN = 0
DUCO_CO2_SETPOINT_RES = 10
DUCO_CO2_SETPOINT_MAX = 2000
DUCO_CO2_SETPOINT_DEFAULT = 800
# duco co2 setpoint
DUCO_RH_SETPOINT_MIN = 0
DUCO_RH_SETPOINT_RES = 5
DUCO_RH_SETPOINT_MAX = 100
DUCO_RH_SETPOINT_DEFAULT = 800
# duco rh delta
DUCO_RH_DELTA_OFF = 0
DUCO_RH_DELTA_ON = 1
# duco flow
DUCO_FLOW_MIN = 20
DUCO_FLOW_RES = 5
DUCO_FLOW_MAX = 200
# duco auto min/max
# only auto defaults, use setpoint min, res, max
DUCO_FAN_SETPOINT_AUTO_MIN_DEFAULT = 10
DUCO_FAN_SETPOINT_AUTO_MAX_DEFAULT = 100
# duco action
# Python enum do not support value of 0, therefore incr register with offset
DUCO_ACTION_OFFSET = 1
DUCO_ACTION_NODE_VISIBILITY_OFF = 0+DUCO_ACTION_OFFSET
DUCO_ACTION_NODE_VISIBILITY_ON = 1+DUCO_ACTION_OFFSET
DUCO_ACTION_ZONE_TO_MANUAL_1 = 2+DUCO_ACTION_OFFSET
DUCO_ACTION_ZONE_TO_MANUAL_2 = 3+DUCO_ACTION_OFFSET
DUCO_ACTION_ZONE_TO_MANUAL_3 = 4+DUCO_ACTION_OFFSET
DUCO_ACTION_ZONE_TO_AUTO = 5+DUCO_ACTION_OFFSET
DUCO_ACTION_AWAY = 6+DUCO_ACTION_OFFSET

# multiple registers have a valid range for percentages of _START,_STEP,_STOP
DUCO_PCT_RANGE_START = 0
DUCO_PCT_RANGE_STEP = 5
DUCO_PCT_RANGE_STOP = 100
