"""Test methods in duco/modbus.py."""
from duco.const import (DUCO_MODULE_TYPE_MASTER)
from duco.enum_types import (ModuleType)
import duco.modbus
import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock


class TestProbeNodeId(unittest.TestCase):
    def test_happyflow(self):
        duco.modbus.MODBUSHUB = MagicMock()
        regMock = MagicMock()
        regMock.registers = [DUCO_MODULE_TYPE_MASTER]
        duco.modbus.MODBUSHUB.read_input_registers.return_value = regMock
        self.assertEqual(duco.modbus.probe_node_id(1), ModuleType(DUCO_MODULE_TYPE_MASTER), "?")
        duco.modbus.MODBUSHUB.read_input_registers.assert_called_once()
        
    def test_sadflow_1(self):
        duco.modbus.MODBUSHUB = MagicMock()
        self.assertFalse(duco.modbus.probe_node_id(1),"")
        duco.modbus.MODBUSHUB.read_input_registers.assert_called_once()

    def test_sadflow_2(self):
        duco.modbus.MODBUSHUB = MagicMock()
        regMock = MagicMock()
        regMock.registers = [1]
        duco.modbus.MODBUSHUB.read_input_registers.return_value = regMock
        self.assertFalse(duco.modbus.probe_node_id(1), "?")
        duco.modbus.MODBUSHUB.read_input_registers.assert_called_once()


class TestToRegisterAddress(unittest.TestCase):
    def test_1(self):
        node_id = 3
        param_id = 5
        self.assertEqual(duco.modbus.to_register_addr(node_id, param_id),
                         (node_id*10+param_id))

    def test_2(self):
        node_id = 9
        param_id = 8
        self.assertEqual(duco.modbus.to_register_addr(node_id, param_id),
                         (node_id*10+param_id))


class TestModbusClose(unittest.TestCase):
    def test(self):
        duco.modbus.MODBUSHUB = Mock()
        duco.modbus.close_modbus()
        duco.modbus.MODBUSHUB.close.assert_called_once()
