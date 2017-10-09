"""Support for Modbus."""
import logging
import struct
import threading

from duco.const import (
    DUCO_REG_ADDR_INPUT_MODULE_TYPE)
from duco.enum_types import (ModuleType)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

# Type of network
CONF_METHOD = 'method'
CONF_HOST = 'host'
CONF_PORT = 'port'
CONF_BAUDRATE = 'baudrate'
CONF_BYTESIZE = 'bytesize'
CONF_STOPBITS = 'stopbits'
CONF_TYPE = 'type'
CONF_PARITY = 'parity'

REGISTER_TYPE_HOLDING = 'holding'
REGISTER_TYPE_INPUT = 'input'

DATA_TYPE_INT = 'int'
DATA_TYPE_FLOAT = 'float'

# Global variable containing Modbus hub
MODBUSHUB = None


def enumerate_module_tree(config):
    """Enumerate Duco module tree."""
    if MODBUSHUB is None:
        setup_modbus(config)

    node_id = 1
    node_found = True

    while node_found:
        _LOGGER.debug("probe node_id %d", node_id)
        result = MODBUSHUB.read_input_registers(
            to_register_addr(node_id, DUCO_REG_ADDR_INPUT_MODULE_TYPE), 1)
        try:
            register = result.registers
        except AttributeError:
            _LOGGER.debug("No response from node_id %d", node_id)
            node_found = False
            break

        module_type = ModuleType(register(0))
        _LOGGER.debug("node_id %d is a module of type %s",
                      node_id, module_type)


def setup_modbus(config):
    """Create and configure Modbus Hub."""
    client_type = config[CONF_TYPE]

    if client_type == 'serial':
        from pymodbus.client.sync import ModbusSerialClient as ModbusClient
        client = ModbusClient(method=config[CONF_METHOD],
                              port=config[CONF_PORT],
                              baudrate=config[CONF_BAUDRATE],
                              stopbits=config[CONF_STOPBITS],
                              bytesize=config[CONF_BYTESIZE],
                              parity=config[CONF_PARITY])
    elif client_type == 'tcp':
        from pymodbus.client.sync import ModbusTcpClient as ModbusClient
        client = ModbusClient(host=config[CONF_HOST],
                              port=config[CONF_PORT])
    else:
        return False

    global MODBUSHUB
    MODBUSHUB = ModbusHub(client)
    # time to connect
    MODBUSHUB.connect()

    return True


def close_modbus():
    """Close Modbus hub."""
    MODBUSHUB.close()


def to_register_addr(node_id, param_id):
    """Compute modbus address from node_id and param_id."""
    return node_id*10 + param_id


class ModbusHub(object):
    """Thread safe wrapper class for pymodbus."""

    def __init__(self, modbus_client):
        """Initialize the modbus hub."""
        self._client = modbus_client
        self._lock = threading.Lock()

    def close(self):
        """Disconnect client."""
        with self._lock:
            self._client.close()

    def connect(self):
        """Connect client."""
        with self._lock:
            self._client.connect()

    def read_coils(self, address, count=1):
        """Read coils."""
        with self._lock:
            return self._client.read_coils(
                address,
                count)

    def read_input_registers(self, address, count=1):
        """Read input registers."""
        with self._lock:
            return self._client.read_input_registers(
                address,
                count)

    def read_holding_registers(self, address, count=1):
        """Read holding registers."""
        with self._lock:
            return self._client.read_holding_registers(
                address,
                count)

    def write_coil(self, address, value):
        """Write coil."""
        with self._lock:
            self._client.write_coil(
                address,
                value)

    def write_register(self, address, value):
        """Write register."""
        with self._lock:
            self._client.write_register(
                address,
                value)

    def write_registers(self, address, values):
        """Write registers."""
        with self._lock:
            self._client.write_registers(
                address,
                values)


class ModbusRegister(object):
    """Modbus register."""

    def __init__(self, name, register, register_type,
                 unit_of_measurement, count, scale, offset, data_type,
                 precision):
        """Initialize the modbus register."""
        self._name = name
        self._register = int(register)
        self._register_type = register_type
        self._unit_of_measurement = unit_of_measurement
        self._count = int(count)
        self._scale = scale
        self._offset = offset
        self._precision = precision
        self._data_type = data_type
        self._value = None

    @property
    def value(self):
        """Return the value of the register."""
        return self._value

    @property
    def name(self):
        """Return the name of the register."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    def update(self):
        """Update the value of the register."""
        if self._register_type == REGISTER_TYPE_INPUT:
            result = MODBUSHUB.read_input_registers(
                self._register,
                self._count)
        else:
            result = MODBUSHUB.read_holding_registers(
                self._register,
                self._count)
        val = 0

        try:
            registers = result.registers
        except AttributeError:
            _LOGGER.error("No response from modbus register %s",
                          self._register)
            return
        if self._data_type == DATA_TYPE_FLOAT:
            byte_string = b''.join(
                [x.to_bytes(2, byteorder='big') for x in registers]
            )
            val = struct.unpack(">f", byte_string)[0]
        elif self._data_type == DATA_TYPE_INT:
            for i, res in enumerate(registers):
                val += res * (2**(i*16))
        self._value = format(
            self._scale * val + self._offset, '.{}f'.format(self._precision))
