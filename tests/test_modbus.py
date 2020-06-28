"""Test methods in duco/modbus.py."""
import unittest
import mock
# from unittest.mock import Mock
from unittest.mock import MagicMock, Mock, PropertyMock, patch
from duco.const import (DUCO_MODULE_TYPE_MASTER)
from duco.enum_types import (ModuleType)
import duco.modbus


class TestCreateClientConfig(unittest.TestCase):
    def test_serial(self):
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0')
        self.assertEqual(client_config[duco.modbus.CONF_TYPE], 'serial')
        self.assertEqual(client_config[duco.modbus.CONF_PORT], '/dev/usb0')

    def test_tcp(self):
        client_config = duco.modbus.create_client_config('tcp', 502)
        self.assertEqual(client_config[duco.modbus.CONF_TYPE], 'tcp')
        self.assertEqual(client_config[duco.modbus.CONF_PORT], '502')

    def test_invalid_client_type(self):
        self.assertRaises(ValueError, lambda: duco.modbus.create_client_config('foo', '/dev/usb0'))
        self.assertRaises(ValueError, lambda: duco.modbus.create_client_config('bar', '/dev/usb0'))


class TestModbusHub(unittest.TestCase):
    def test_init(self):
        # serial
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0')
        hub = duco.modbus.ModbusHub(client_config)

        self.assertEqual(hub._client, None, "")
        self.assertEqual(hub._kwargs, {'unit': client_config[duco.modbus.CONF_MASTER_UNIT_ID]}, "")
        self.assertEqual(hub._config_type, client_config[duco.modbus.CONF_TYPE], "")
        self.assertEqual(hub._config_port, client_config[duco.modbus.CONF_PORT], "")
        self.assertRaises(AttributeError, lambda: hub._config_host)
        self.assertEqual(hub._config_timeout, client_config[duco.modbus.CONF_TIMEOUT], "")
        self.assertEqual(hub._config_delay, 0, "")
        self.assertEqual(hub._config_method, client_config[duco.modbus.CONF_METHOD], "")
        self.assertEqual(hub._config_baudrate, client_config[duco.modbus.CONF_BAUDRATE], "")
        self.assertEqual(hub._config_stopbits, client_config[duco.modbus.CONF_STOPBITS], "")
        self.assertEqual(hub._config_bytesize, client_config[duco.modbus.CONF_BYTESIZE], "")
        self.assertEqual(hub._config_parity, client_config[duco.modbus.CONF_PARITY], "")

        # tcp
        client_config = duco.modbus.create_client_config('tcp', 502, '192.168.0.1')
        hub = duco.modbus.ModbusHub(client_config)

        self.assertEqual(hub._client, None, "")
        self.assertEqual(hub._kwargs, {'unit': client_config[duco.modbus.CONF_MASTER_UNIT_ID]}, "")
        self.assertEqual(hub._config_type, client_config[duco.modbus.CONF_TYPE], "")
        self.assertEqual(hub._config_port, client_config[duco.modbus.CONF_PORT], "")
        self.assertEqual(hub._config_host, client_config[duco.modbus.CONF_HOST], "")
        self.assertEqual(hub._config_timeout, client_config[duco.modbus.CONF_TIMEOUT], "")
        self.assertEqual(hub._config_delay, 0, "")
        self.assertRaises(AttributeError, lambda: hub._config_method)
        self.assertRaises(AttributeError, lambda: hub._config_baudrate)
        self.assertRaises(AttributeError, lambda: hub._config_stopbits)
        self.assertRaises(AttributeError, lambda: hub._config_bytesize)
        self.assertRaises(AttributeError, lambda: hub._config_parity)

        # incorrect type
        self.assertRaises(ValueError, lambda: duco.modbus.create_client_config('some', '/dev/usb0'))

    @patch('pymodbus.client.sync.ModbusRtuFramer')
    @patch('pymodbus.client.sync.ModbusSerialClient')
    @patch('pymodbus.client.sync.ModbusTcpClient')
    @patch('pymodbus.client.sync.ModbusUdpClient')
    def test_setup(self, udp_client, tcp_client, serial_client, rtu_framer):
        # serial
        client_config = duco.modbus.create_client_config('serial', '/dev/usb0')
        hub = duco.modbus.ModbusHub(client_config)
        hub.setup()
        hub._client.connect.assert_called_once()

        # rtuovertcp
        client_config = duco.modbus.create_client_config('rtuovertcp', 500, '192.168.0.1')
        hub = duco.modbus.ModbusHub(client_config)
        hub.setup()
        hub._client.connect.assert_called_once()
      
        # tcp
        client_config = duco.modbus.create_client_config('tcp', 501, '192.168.0.2')
        hub = duco.modbus.ModbusHub(client_config)
        hub.setup()
        #hub._client.connect.assert_called_once()

        # udp
        client_config = duco.modbus.create_client_config('udp', 502, '192.168.0.3')
        hub = duco.modbus.ModbusHub(client_config)
        hub.setup()
        hub._client.connect.assert_called_once()

        # incorrect type
        client_config = {duco.modbus.CONF_TYPE: 'some_type',
                         duco.modbus.CONF_PORT: '403',
                         duco.modbus.CONF_MASTER_UNIT_ID: int(0),
                         duco.modbus.CONF_TIMEOUT: int(3),
                         duco.modbus.CONF_HOST: 'some_host'}
        hub = duco.modbus.ModbusHub(client_config)
        self.assertRaises(ValueError, lambda: hub.setup())

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
    def test_init_minimal(self):
        r_hub = MagicMock()
        r_name = 'MyName'
        r_reg_addr = 10
        r_reg_type = duco.modbus.REGISTER_TYPE_INPUT
        reg = duco.modbus.ModbusRegister(r_hub, r_name, r_reg_addr,
                                         r_reg_type)
        self.assertEqual(reg.name, r_name, "")
        self.assertEqual(reg._register_addr, r_reg_addr)
        self.assertEqual(reg._register_type, r_reg_type)
        self.assertEqual(reg.unit_of_measurement, "", "")
        self.assertEqual(reg._scale, 1)
        self.assertEqual(reg._offset, 0)
        self.assertEqual(reg._precision, 0)
        self.assertEqual(reg._count, 1)
        self.assertEqual(reg._value, None)

    def test_init_full(self):
        r_hub = MagicMock()
        r_name = 'SomeName'
        r_reg_addr = 3
        r_reg_type = duco.modbus.REGISTER_TYPE_HOLDING
        r_unit = 'ppm'
        r_scale = 2
        r_offset = 3
        r_precision = 4
        reg = duco.modbus.ModbusRegister(r_hub, r_name, r_reg_addr,
                                         r_reg_type, r_unit,
                                         r_scale, r_offset, r_precision)
        self.assertEqual(reg.name, r_name, "")
        self.assertEqual(reg._register_addr, r_reg_addr)
        self.assertEqual(reg._register_type, r_reg_type)
        self.assertEqual(reg.unit_of_measurement, r_unit, "")
        self.assertEqual(reg._scale, r_scale)
        self.assertEqual(reg._offset, r_offset)
        self.assertEqual(reg._precision, r_precision)
        self.assertEqual(reg._count, 1)
        self.assertEqual(reg._value, None)

    def test_get_value_holding_1(self):
        mock_result = MagicMock(spec=['registers'])
        registers = PropertyMock(return_value=[216])
        type(mock_result).registers = registers
        mock_hub = MagicMock(spec=['read_holding_registers'])
        mock_hub.read_holding_registers.return_value = mock_result

        r_name = 'SomeName'
        r_reg_addr = 3
        r_reg_type = duco.modbus.REGISTER_TYPE_HOLDING
        r_unit = 'ppm'
        r_scale = 0.1
        r_offset = 0
        r_precision = 1
        reg = duco.modbus.ModbusRegister(mock_hub, r_name, r_reg_addr,
                                         r_reg_type, r_unit,
                                         r_scale, r_offset, r_precision)
        value = reg.value
        state = reg.state
        str_reg = str(reg)
        mock_hub.read_holding_registers.assert_called_with(r_reg_addr, 1)
        self.assertEqual(mock_hub.read_holding_registers.call_count, 3)

        self.assertEqual(value, "21.6")
        self.assertEqual(state['value'], "21.6")
        self.assertEqual(state['name'], r_name)
        self.assertEqual(state['unit'], r_unit)
        self.assertEqual(str_reg, r_name+ ': '+ str(value)+' '+r_unit)

    def test_get_value_holding_2(self):
        mock_result = MagicMock(spec=['registers'])
        registers = PropertyMock(return_value=[3754])
        type(mock_result).registers = registers
        mock_hub = MagicMock(spec=['read_holding_registers'])
        mock_hub.read_holding_registers.return_value = mock_result

        r_name = 'SomeName'
        r_reg_addr = 3
        r_reg_type = duco.modbus.REGISTER_TYPE_HOLDING
        r_unit = 'ppm'
        r_scale = 0.01
        r_offset = 0
        r_precision = 2
        reg = duco.modbus.ModbusRegister(mock_hub, r_name, r_reg_addr,
                                         r_reg_type, r_unit,
                                         r_scale, r_offset, r_precision)
        value = reg.value
        mock_hub.read_holding_registers.assert_called_once_with(r_reg_addr, 1)
        self.assertEqual(value, "37.54")

    def test_get_value_input_1(self):
        mock_result = MagicMock(spec=['registers'])
        registers = PropertyMock(return_value=[216])
        type(mock_result).registers = registers
        mock_hub = MagicMock(spec=['read_input_registers'])
        mock_hub.read_input_registers.return_value = mock_result

        r_name = 'SomeName'
        r_reg_addr = 3
        r_reg_type = duco.modbus.REGISTER_TYPE_INPUT
        r_unit = 'ppm'
        r_scale = 0.1
        r_offset = 0
        r_precision = 1
        reg = duco.modbus.ModbusRegister(mock_hub, r_name, r_reg_addr,
                                         r_reg_type, r_unit,
                                         r_scale, r_offset, r_precision)
        value = reg.value
        mock_hub.read_input_registers.assert_called_once_with(r_reg_addr, 1)
        self.assertEqual(value, "21.6")

    def test_get_value_input_2(self):
        mock_result = MagicMock(spec=['registers'])
        registers = PropertyMock(return_value=[3754])
        type(mock_result).registers = registers
        mock_hub = MagicMock(spec=['read_input_registers'])
        mock_hub.read_input_registers.return_value = mock_result

        r_name = 'SomeName'
        r_reg_addr = 3
        r_reg_type = duco.modbus.REGISTER_TYPE_INPUT
        r_unit = 'ppm'
        r_scale = 0.01
        r_offset = 0
        r_precision = 2
        reg = duco.modbus.ModbusRegister(mock_hub, r_name, r_reg_addr,
                                         r_reg_type, r_unit,
                                         r_scale, r_offset, r_precision)
        value = reg.value
        mock_hub.read_input_registers.assert_called_once_with(r_reg_addr, 1)
        self.assertEqual(value, "37.54")

    def test_get_value_raises(self):
        # correct result
        mock_result_ok = MagicMock(spec=['registers'])
        registers = PropertyMock(return_value=[3754])
        type(mock_result_ok).registers = registers
        # no result (raises AttributeError)
        mock_result_attrerror = MagicMock(spec=[])
        mock_hub = MagicMock(spec=['read_input_registers'])

        r_name = 'SomeName'
        r_reg_addr = 3
        r_reg_type = duco.modbus.REGISTER_TYPE_INPUT
        r_unit = 'ppm'
        r_scale = 0.01
        r_offset = 0
        r_precision = 2
        reg = duco.modbus.ModbusRegister(mock_hub, r_name, r_reg_addr,
                                         r_reg_type, r_unit,
                                         r_scale, r_offset, r_precision)

        # 1. no result
        mock_hub.read_input_registers.return_value = mock_result_attrerror
        self.assertEqual(reg.value, None)
        # 2. correct result
        mock_hub.read_input_registers.return_value = mock_result_ok
        self.assertEqual(reg.value, "37.54")
        # 3. no result from modbus, should return previous value
        mock_hub.read_input_registers.return_value = mock_result_attrerror
        self.assertEqual(reg.value, "37.54")

    def test_set_value_holding(self):
        mock_hub = MagicMock(spec=['write_register'])
        r_name = 'SomeName'
        r_reg_addr = 3
        r_reg_type = duco.modbus.REGISTER_TYPE_HOLDING
        r_unit = 'ppm'
        r_scale = 0.01
        r_offset = 0
        r_precision = 2
        reg = duco.modbus.ModbusRegister(mock_hub, r_name, r_reg_addr,
                                         r_reg_type, r_unit,
                                         r_scale, r_offset, r_precision)

        reg.value = 100
        mock_hub.write_register.assert_called_once_with(r_reg_addr, 100)

    def test_set_value_input(self):
        mock_hub = MagicMock(spec=['write_register'])
        r_name = 'SomeName'
        r_reg_addr = 3
        r_reg_type = duco.modbus.REGISTER_TYPE_INPUT
        r_unit = 'ppm'
        r_scale = 0.01
        r_offset = 0
        r_precision = 2
        reg = duco.modbus.ModbusRegister(mock_hub, r_name, r_reg_addr,
                                         r_reg_type, r_unit,
                                         r_scale, r_offset, r_precision)

        with self.assertRaises(TypeError):
            reg.value = 100
