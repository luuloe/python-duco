"""Support for Modbus."""
import logging
import struct
import threading

from duco.const import (
    PROJECT_PACKAGE_NAME)

_LOGGER = logging.getLogger(PROJECT_PACKAGE_NAME)

# Type of network
CONF_MASTER_UNIT_ID = 'master_unit_id'
CONF_METHOD = 'method'
CONF_HOST = 'host'
CONF_PORT = 'port'
CONF_BAUDRATE = 'baudrate'
CONF_BYTESIZE = 'bytesize'
CONF_STOPBITS = 'stopbits'
CONF_TYPE = 'type'
CONF_PARITY = 'parity'
CONF_TIMEOUT = 'timeout'

REGISTER_TYPE_HOLDING = 'holding'
REGISTER_TYPE_INPUT = 'input'

DATA_TYPE_INT = 'int'
DATA_TYPE_FLOAT = 'float'


def to_register_addr(node_id, param_id):
    """Compute modbus address from node_id and param_id."""
    return node_id*10 + param_id


class ModbusHub:
    """Thread safe wrapper class for pymodbus."""

    def __init__(self, client_config):
        """Initialize the modbus hub."""

        # generic configuration
        self._client = None
        self._kwargs = {'unit': client_config[CONF_MASTER_UNIT_ID]}
        self._lock = threading.Lock()
        self._config_type = client_config[CONF_TYPE]
        self._config_port = client_config[CONF_PORT]
        self._config_timeout = client_config[CONF_TIMEOUT]
        self._config_delay = 0

        if self._config_type == "serial":
            # serial configuration
            self._config_method = client_config[CONF_METHOD]
            self._config_baudrate = client_config[CONF_BAUDRATE]
            self._config_stopbits = client_config[CONF_STOPBITS]
            self._config_bytesize = client_config[CONF_BYTESIZE]
            self._config_parity = client_config[CONF_PARITY]
        else:
            # network configuration
            self._config_host = client_config[CONF_HOST]

    def setup(self):
        """Set up pymodbus client."""
        if self._config_type == "serial":
            from pymodbus.client.sync import ModbusSerialClient
            self._client = ModbusSerialClient(
                method=self._config_method,
                port=self._config_port,
                baudrate=self._config_baudrate,
                stopbits=self._config_stopbits,
                bytesize=self._config_bytesize,
                parity=self._config_parity,
                timeout=self._config_timeout,
                retry_on_empty=True,
            )
        elif self._config_type == "rtuovertcp":
            from pymodbus.client.sync import ModbusTcpClient
            from pymodbus.transaction import ModbusRtuFramer
            self._client = ModbusTcpClient(
                host=self._config_host,
                port=self._config_port,
                framer=ModbusRtuFramer,
                timeout=self._config_timeout,
            )
        elif self._config_type == "tcp":
            from pymodbus.client.sync import ModbusTcpClient
            self._client = ModbusTcpClient(
                host=self._config_host,
                port=self._config_port,
                timeout=self._config_timeout,
            )
        elif self._config_type == "udp":
            from pymodbus.client.sync import ModbusUdpClient
            self._client = ModbusUdpClient(
                host=self._config_host,
                port=self._config_port,
                timeout=self._config_timeout,
            )
        else:
            assert False

        # Connect device
        self.connect()

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
                count,
                **self._kwargs)

    def read_input_registers(self, address, count=1):
        """Read input registers."""
        with self._lock:
            return self._client.read_input_registers(
                address,
                count,
                **self._kwargs)

    def read_holding_registers(self, address, count=1):
        """Read holding registers."""
        with self._lock:
            return self._client.read_holding_registers(
                address,
                count,
                **self._kwargs)

    def write_coil(self, address, value):
        """Write coil."""
        with self._lock:
            self._client.write_coil(
                address,
                value,
                **self._kwargs)

    def write_register(self, address, value):
        """Write register."""
        with self._lock:
            self._client.write_register(
                address,
                value,
                **self._kwargs)

    def write_registers(self, address, values):
        """Write registers."""
        with self._lock:
            self._client.write_registers(
                address,
                values,
                **self._kwargs)


class ModbusRegister:
    """Modbus register."""

    def __init__(self, hub, name, register, register_type,
                 unit_of_measurement, count, scale, offset, data_type,
                 precision):
        """Initialize the modbus register."""
        self._hub = hub
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
    def state(self):
        """Return the state of the register."""
        self.update()
        return {'name': self._name,
                'value': self._value,
                'unit': self._unit_of_measurement}

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
            result = self._hub.read_input_registers(
                self._register,
                self._count)
        else:
            result = self._hub.read_holding_registers(
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
