"""Duco nodes supported by python-duco."""
from duco.const import (DUCO_REG_ADDR_INPUT_STATUS, 
                        DUCO_REG_ADDR_INPUT_FAN_ACTUAL,
                        DUCO_REG_ADDR_HOLD_FAN_SETPOINT,
                        DUCO_REG_ADDR_HOLD_AUTOMIN,
                        DUCO_REG_ADDR_HOLD_AUTOMAX,
                        DUCO_REG_ADDR_HOLD_ACTION)
from duco.enum_types import (ModuleType, ZoneStatus, ZoneAction)
from duco.modbus import (REGISTER_TYPE_INPUT, REGISTER_TYPE_HOLDING, 
                         DATA_TYPE_INT, 
                         to_register_address, ModbusRegister)

class Node(object):
    """Duco base node."""
    # Create based on ModuleType:
    def factory(node_id, node_type):
        """Factory function for all Node types."""
        if node_type == ModuleType.MASTER: return Box(node_id, node_type)
        assert 0, "Bad node creation: " + node_type
    factory = staticmethod(factory)
    
    def __init__(self, node_id, node_type):
        """Example of docstring on the __init__ method."""
        self._node_id = int(node_id)
        self._node_type = ModuleType(node_type)
        self._child_nodes = []
        # registers
        # name, register, register_type,
        # unit_of_measurement, count, scale, offset, data_type, precision
        # input
        self._reg_status = ModbusRegister(
            'Zone status',
            to_register_address(self._node_id, DUCO_REG_ADDR_INPUT_STATUS),
            REGISTER_TYPE_INPUT, '', 1, 1, 1, DATA_TYPE_INT, 0)
        
        self._reg_status = ModbusRegister(
            'Fan actual',
            to_register_address(self._node_id, DUCO_REG_ADDR_INPUT_FAN_ACTUAL), 
            REGISTER_TYPE_INPUT, '%', 1, 1, 1, DATA_TYPE_INT, 0)
        # holding
        self._reg_setpoint = ModbusRegister(
            'Zone setpoint',
            to_register_address(self._node_id, DUCO_REG_ADDR_HOLD_FAN_SETPOINT), 
            REGISTER_TYPE_HOLDING, '%', 1, 1, 1, DATA_TYPE_INT, 0)
        
        self._reg_action = ModbusRegister(
            'Zone action',
            to_register_address(self._node_id, DUCO_REG_ADDR_HOLD_ACTION), 
            REGISTER_TYPE_HOLDING, '', 1, 1, 1, DATA_TYPE_INT, 0)
    
    @property
    def node_id(self):
        """Return the id of the node."""
        return self._node_id
    
    @property
    def node_type(self):
        """Return the type of the node."""
        return self._node_type
    
    @property
    def action(self):
        """Return the zone action of the node."""
        # synchronous update for now
        self._reg_action.update()
        return ZoneAction(self._reg_action.value())
    
    @property
    def status(self):
        """Return the zone status of the node."""
        # synchronous update for now
        self._reg_status.update()
        return ZoneStatus(self._reg_status.value())

class AutoMinMax(object):
    """Duco node containing AutoMin and AutoMax registers."""
    def __init__(self, node_id):
        """Example of docstring on the __init__ method."""
        self._reg_automin = ModbusRegister(
            'AutoMin',
            to_register_address(node_id, DUCO_REG_ADDR_HOLD_AUTOMIN),
            REGISTER_TYPE_HOLDING, '%', 1, 1, 1, DATA_TYPE_INT, 0)
        
        self._reg_automax = ModbusRegister(
            'AutoMax',
            to_register_address(node_id, DUCO_REG_ADDR_HOLD_AUTOMAX),
            REGISTER_TYPE_HOLDING, '%', 1, 1, 1, DATA_TYPE_INT, 0)
    
    @property
    def auto_min(self):
        """Return the auto min of the node."""
        # synchronous update for now
        self._reg_automin.update()
        return int(self._reg_automin.value())
    
    @property
    def auto_max(self):
        """Return the auto max of the node."""
        # synchronous update for now
        self._reg_automax.update()
        return int(self._reg_automax.value())

class Box(Node, AutoMinMax):
    """Duco box node."""
    def __init__(self, node_id, node_type):
        """Example of docstring on the __init__ method."""
        super(Node, self).__init__(node_id, node_type)
        super(AutoMinMax, self).__init__(node_id)
        # no additional registers
