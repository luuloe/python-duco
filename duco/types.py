"""Types used by python-duco."""
from enum import IntEnum, unique
from duco.const import (
    DUCO_MODULE_TYPE_MASTER, DUCO_MODULE_TYPE_VALVE_SENSORLESS,
    DUCO_MODULE_TYPE_VALVE_CO2, DUCO_MODULE_TYPE_VALVE_RH,
    DUCO_MODULE_TYPE_USER_CONTROLLER,
    DUCO_MODULE_TYPE_ROOM_SENSOR_CO2, DUCO_MODULE_TYPE_ROOM_SENSOR_RH,
    DUCO_MODULE_TYPE_CTRL_WINDOW_VENT, DUCO_MODULE_TYPE_ROOM_SWITCH,
    DUCO_MODULE_TYPE_ACTUATOR_PRINT,
    DUCO_ZONE_STATUS_AUTO, DUCO_ZONE_STATUS_HIGH_10MIN,
    DUCO_ZONE_STATUS_HIGH_20MIN, DUCO_ZONE_STATUS_HIGH_30MIN,
    DUCO_ZONE_STATUS_MANUAL_LOW, DUCO_ZONE_STATUS_MANUAL_MEDIUM,
    DUCO_ZONE_STATUS_MANUAL_HIGH, DUCO_ZONE_STATUS_AWAY, 
    DUCO_ZONE_STATUS_ERROR,
    DUCO_ACTION_NODE_VISIBILITY_OFF, DUCO_ACTION_NODE_VISIBILITY_ON,
    DUCO_ACTION_ZONE_TO_MANUAL_1, DUCO_ACTION_ZONE_TO_MANUAL_2,
    DUCO_ACTION_ZONE_TO_MANUAL_3, DUCO_ACTION_ZONE_TO_AUTO, DUCO_ACTION_AWAY)

@unique
class ModuleType(IntEnum):
    """ModuleType enumeration."""
    MASTER = DUCO_MODULE_TYPE_MASTER
    VALVE_SENSORLESS = DUCO_MODULE_TYPE_VALVE_SENSORLESS
    VALVE_CO2 = DUCO_MODULE_TYPE_VALVE_CO2
    VALVE_RH = DUCO_MODULE_TYPE_VALVE_RH
    USER_CONTROLLER = DUCO_MODULE_TYPE_USER_CONTROLLER
    ROOM_SENSOR_CO2 = DUCO_MODULE_TYPE_ROOM_SENSOR_CO2
    ROOM_SENSOR_RH = DUCO_MODULE_TYPE_ROOM_SENSOR_RH
    CTRL_WINDOW_VENT = DUCO_MODULE_TYPE_CTRL_WINDOW_VENT
    ROOM_SWITCH = DUCO_MODULE_TYPE_ROOM_SWITCH
    ACTUATOR_PRINT = DUCO_MODULE_TYPE_ACTUATOR_PRINT

@unique
class ZoneStatus(IntEnum):
    """ZoneStatus enumeration."""
    AUTO = DUCO_ZONE_STATUS_AUTO
    HIGH_10MIN = DUCO_ZONE_STATUS_HIGH_10MIN
    HIGH_20MIN = DUCO_ZONE_STATUS_HIGH_20MIN
    HIGH_30MIN = DUCO_ZONE_STATUS_HIGH_30MIN
    MANUAL_LOW = DUCO_ZONE_STATUS_MANUAL_LOW
    MANUAL_MEDIUM = DUCO_ZONE_STATUS_MANUAL_MEDIUM
    MANUAL_HIGH = DUCO_ZONE_STATUS_MANUAL_HIGH
    AWAY = DUCO_ZONE_STATUS_AWAY
    ERROR = DUCO_ZONE_STATUS_ERROR

@unique
class ZoneAction(IntEnum):
    """ZoneAction enumeration."""
    NODE_VISIBILITY_OFF = DUCO_ACTION_NODE_VISIBILITY_OFF
    NODE_VISIBILITY_ON = DUCO_ACTION_NODE_VISIBILITY_ON
    ZONE_TO_MANUAL_1 = DUCO_ACTION_ZONE_TO_MANUAL_1
    ZONE_TO_MANUAL_2 = DUCO_ACTION_ZONE_TO_MANUAL_2
    ZONE_TO_MANUAL_3 = DUCO_ACTION_ZONE_TO_MANUAL_3
    ZONE_TO_AUTO = DUCO_ACTION_ZONE_TO_AUTO
    AWAY = DUCO_ACTION_AWAY
