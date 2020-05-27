"""Test methods in duco/modbus.py."""
import unittest
# from unittest.mock import Mock
from unittest.mock import MagicMock
from duco.const import (DUCO_MODULE_TYPE_MASTER)
from duco.enum_types import (ModuleType)
import duco.modbus


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


class TestModbusHub(unittest.TestCase):
    def test_init_1(self):
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0')
        hub = duco.modbus.ModbusHub(client_config)

        self.assertEqual(hub._client, None, "")
        self.assertEqual(hub._kwargs, {'unit': client_config[duco.modbus.CONF_MASTER_UNIT_ID]}, "")
        self.assertEqual(hub._config_type, client_config[duco.modbus.CONF_TYPE], "")
        self.assertEqual(hub._config_port, client_config[duco.modbus.CONF_PORT], "")
        self.assertEqual(hub._config_timeout, client_config[duco.modbus.CONF_TIMEOUT], "")
        self.assertEqual(hub._config_delay, 0, "")
        self.assertEqual(hub._config_method, client_config[duco.modbus.CONF_METHOD], "")
        self.assertEqual(hub._config_baudrate, client_config[duco.modbus.CONF_BAUDRATE], "")
        self.assertEqual(hub._config_stopbits, client_config[duco.modbus.CONF_STOPBITS], "")
        self.assertEqual(hub._config_bytesize, client_config[duco.modbus.CONF_BYTESIZE], "")
        self.assertEqual(hub._config_parity, client_config[duco.modbus.CONF_PARITY], "")

    def test_close(self):
        modbus_client = MagicMock()
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0')
        hub = duco.modbus.ModbusHub(client_config)
        hub._client = modbus_client
        hub.close()
        modbus_client.close.assert_called_once()

    def test_connect(self):
        modbus_client = MagicMock()
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0')
        hub = duco.modbus.ModbusHub(client_config)
        hub._client = modbus_client
        hub.connect()
        modbus_client.connect.assert_called_once()

    def test_read_coils(self):
        master_id = 10
        modbus_client = MagicMock()
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0', None, master_id)
        hub = duco.modbus.ModbusHub(client_config)
        hub._client = modbus_client
        address = 42
        count = 3
        hub.read_coils(address, count)
        modbus_client.read_coils.assert_called_with(address, count, unit=master_id)
        hub.read_coils(address)
        modbus_client.read_coils.assert_called_with(address, 1, unit=master_id)

    def test_read_input_registers(self):
        master_id = 10
        modbus_client = MagicMock()
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0', None, master_id)
        hub = duco.modbus.ModbusHub(client_config)
        hub._client = modbus_client
        address = 42
        count = 3
        hub.read_input_registers(address, count)
        modbus_client.read_input_registers.assert_called_with(address, count, unit=master_id)
        hub.read_input_registers(address)
        modbus_client.read_input_registers.assert_called_with(address, 1, unit=master_id)

    def test_read_holding_registers(self):
        master_id = 10
        modbus_client = MagicMock()
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0', None, master_id)
        hub = duco.modbus.ModbusHub(client_config)
        hub._client = modbus_client
        address = 42
        count = 3
        hub.read_holding_registers(address, count)
        modbus_client.read_holding_registers.assert_called_with(address, count, unit=master_id)
        hub.read_holding_registers(address)
        modbus_client.read_holding_registers.assert_called_with(address, 1, unit=master_id)

    def test_write_coil(self):
        master_id = 10
        modbus_client = MagicMock()
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0', None, master_id)
        hub = duco.modbus.ModbusHub(client_config)
        hub._client = modbus_client
        address = 42
        value = 3
        hub.write_coil(address, value)
        modbus_client.write_coil.assert_called_once_with(address, value, unit=master_id)

    def test_write_register(self):
        master_id = 10
        modbus_client = MagicMock()
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0', None, master_id)
        hub = duco.modbus.ModbusHub(client_config)
        hub._client = modbus_client
        address = 42
        value = 3
        hub.write_register(address, value)
        modbus_client.write_register.assert_called_once_with(address, value, unit=master_id)

    def test_write_registers(self):
        master_id = 10
        modbus_client = MagicMock()
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0', None, master_id)
        hub = duco.modbus.ModbusHub(client_config)
        hub._client = modbus_client
        address = 42
        value = 3
        hub.write_registers(address, value)
        modbus_client.write_registers.assert_called_once_with(address, value, unit=master_id)


class TestModbusRegister(unittest.TestCase):
    def test_init(self):
        r_hub = MagicMock()
        r_name = 'Zone'
        r_reg = 10
        r_reg_type = duco.modbus.REGISTER_TYPE_INPUT
        r_unit = ''
        r_count = 1
        r_scale = 2
        r_offset = 3
        r_data_type = duco.modbus.DATA_TYPE_INT
        r_precision = 4
        reg = duco.modbus.ModbusRegister(r_hub, r_name, r_reg, r_reg_type, r_unit,
                                       r_count, r_scale, r_offset, r_data_type,
                                       r_precision)
        self.assertEqual(reg.name, r_name, "")
        self.assertEqual(reg.unit_of_measurement, r_unit, "")
        self.assertEqual(reg.value, None)
        self.assertEqual(reg._count, r_count)
        self.assertEqual(reg._scale, r_scale)
        self.assertEqual(reg._offset, r_offset)
        self.assertEqual(reg._data_type, r_data_type)
        self.assertEqual(reg._precision, r_precision)
