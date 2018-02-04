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
        self.assertEqual(duco.modbus.probe_node_id(1),
                         ModuleType(DUCO_MODULE_TYPE_MASTER), "?")
        duco.modbus.MODBUSHUB.read_input_registers.assert_called_once()

    def test_sadflow_1(self):
        duco.modbus.MODBUSHUB = MagicMock()
        self.assertFalse(duco.modbus.probe_node_id(1), "")
        duco.modbus.MODBUSHUB.read_input_registers.assert_called_once()

    def test_sadflow_2(self):
        duco.modbus.MODBUSHUB = MagicMock()
        regMock = MagicMock()
        regMock.registers = [1]
        duco.modbus.MODBUSHUB.read_input_registers.return_value = regMock
        self.assertFalse(duco.modbus.probe_node_id(1), "?")
        duco.modbus.MODBUSHUB.read_input_registers.assert_called_once()

    def test_sadflow_3(self):
        duco.modbus.MODBUSHUB = MagicMock()
        regMock = MagicMock()
        regMock.registers.side_effect = AttributeError
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


class TestModbusHub(unittest.TestCase):
    def test_init(self):
        c = MagicMock()
        id = 10
        hub = duco.modbus.ModbusHub(c, id)
        self.assertEqual(hub._client, c, "")
        self.assertEqual(hub._kwargs, {'unit': id}, "")

    def test_close(self):
        c = MagicMock()
        id = 10
        hub = duco.modbus.ModbusHub(c, id)
        hub.close()
        c.close.assert_called_once()

    def test_connect(self):
        c = MagicMock()
        id = 10
        hub = duco.modbus.ModbusHub(c, id)
        hub.connect()
        c.connect.assert_called_once()

    def test_read_coils(self):
        c = MagicMock()
        id = 10
        hub = duco.modbus.ModbusHub(c, id)
        address = 42
        count = 3
        hub.read_coils(address, count)
        c.read_coils.assert_called_with(address, count, unit=id)
        hub.read_coils(address)
        c.read_coils.assert_called_with(address, 1, unit=id)

    def test_read_input_registers(self):
        c = MagicMock()
        id = 10
        hub = duco.modbus.ModbusHub(c, id)
        address = 42
        count = 3
        hub.read_input_registers(address, count)
        c.read_input_registers.assert_called_with(address, count, unit=id)
        hub.read_input_registers(address)
        c.read_input_registers.assert_called_with(address, 1, unit=id)

    def test_read_holding_registers(self):
        c = MagicMock()
        id = 10
        hub = duco.modbus.ModbusHub(c, id)
        address = 42
        count = 3
        hub.read_holding_registers(address, count)
        c.read_holding_registers.assert_called_with(address, count, unit=id)
        hub.read_holding_registers(address)
        c.read_holding_registers.assert_called_with(address, 1, unit=id)

    def test_write_coil(self):
        c = MagicMock()
        id = 10
        hub = duco.modbus.ModbusHub(c, id)
        address = 42
        value = 3
        hub.write_coil(address, value)
        c.write_coil.assert_called_once_with(address, value, unit=id)

    def test_write_register(self):
        c = MagicMock()
        id = 10
        hub = duco.modbus.ModbusHub(c, id)
        address = 42
        value = 3
        hub.write_register(address, value)
        c.write_register.assert_called_once_with(address, value, unit=id)

    def test_write_registers(self):
        c = MagicMock()
        id = 10
        hub = duco.modbus.ModbusHub(c, id)
        address = 42
        value = 3
        hub.write_registers(address, value)
        c.write_registers.assert_called_once_with(address, value, unit=id)


class TestModbusRegister(unittest.TestCase):
    def test_init(self):
        r_name = 'Zone'
        r_reg = 10
        r_reg_type = duco.modbus.REGISTER_TYPE_INPUT
        r_unit = ''
        r_count = 1
        r_scale = 2
        r_offset = 3
        r_data_type = duco.modbus.DATA_TYPE_INT
        r_precision = 4
        r = duco.modbus.ModbusRegister(r_name, r_reg, r_reg_type, r_unit,
                                       r_count, r_scale, r_offset, r_data_type,
                                       r_precision)
        self.assertEqual(r.name, r_name, "")
        self.assertEqual(r.unit_of_measurement, r_unit, "")
        self.assertEqual(r.value, None)
        self.assertEqual(r._count, r_count)
        self.assertEqual(r._scale, r_scale)
        self.assertEqual(r._offset, r_offset)
        self.assertEqual(r._data_type, r_data_type)
        self.assertEqual(r._precision, r_precision)
