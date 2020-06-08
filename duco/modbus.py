"""Support for Modbus."""
import logging
import struct
import threading

from duco.const import (
    PROJECT_PACKAGE_NAME,
    DUCO_MODBUS_BAUD_RATE,
    DUCO_MODBUS_BYTE_SIZE,
    DUCO_MODBUS_STOP_BITS,
    DUCO_MODBUS_PARITY,
    DUCO_MODBUS_METHOD
)
from duco.helpers import (twos_comp)

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


def create_client_config(modbus_client_type, modbus_client_port,
                         modbus_client_host=None, modbus_master_unit_id=0):
    """Create config dictionary."""
    config = {CONF_TYPE: str(modbus_client_type),
              CONF_PORT: str(modbus_client_port),
              CONF_MASTER_UNIT_ID: int(modbus_master_unit_id),
              CONF_TIMEOUT: int(3)}
    # type specific part
    if modbus_client_type == 'serial':
        config[CONF_METHOD] = DUCO_MODBUS_METHOD
        config[CONF_BAUDRATE] = DUCO_MODBUS_BAUD_RATE
        config[CONF_BYTESIZE] = DUCO_MODBUS_BYTE_SIZE
        config[CONF_STOPBITS] = DUCO_MODBUS_STOP_BITS
        config[CONF_PARITY] = DUCO_MODBUS_PARITY
    elif modbus_client_type == 'tcp':
        config[CONF_HOST] = str(modbus_client_host)
    else:
        raise ValueError("modbus_client_type must be serial or tcp")

    return config


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
            raise ValueError(("Unsupported config_type, must be serial, " +
                              "tcp, udp, rtuovertcp"))

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

    def __str__(self):
        """Return the string representation of the register."""
        return (self._name + ": " + str(self.value) + " " +
                self._unit_of_measurement)

    @property
    def value(self):
        """Return the value of the register."""
        self.update()
        return self._value

    @value.setter
    def value(self, new_value):
        """Set the value of the node to new_value."""
        if self._register_type != REGISTER_TYPE_HOLDING:
            raise TypeError("Register must be of type HOLDING")

        self._hub.write_register(self._register, new_value)

    @property
    def state(self):
        """Return the state of the register."""
        return {'name': self._name,
                'value': str(self.value),
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
        """Update the value of the register from the external hub."""
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
            for _, res in enumerate(registers):
                val += twos_comp(res, 16)
        self._value = format(
            self._scale * val + self._offset, '.{}f'.format(self._precision))
