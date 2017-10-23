"""Duco."""
from duco.const import (
    DUCO_MODBUS_MASTER_DEFAULT_UNIT_ID, DUCO_MODBUS_BAUD_RATE,
    DUCO_MODBUS_BYTE_SIZE, DUCO_MODBUS_STOP_BITS,
    DUCO_MODBUS_PARITY, DUCO_MODBUS_METHOD)

from duco.modbus import (CONF_TYPE, CONF_PORT, CONF_MASTER_UNIT_ID,
                         CONF_BAUDRATE, CONF_BYTESIZE, CONF_STOPBITS,
                         CONF_PARITY, CONF_HOST, CONF_METHOD,
                         setup_modbus, close_modbus)

from duco.nodes import (enumerate_node_tree)


def create_config(modbus_client_type, modbus_client_port,
                  modbus_master_unit_id):
    """Create config dictionary."""
    config = {CONF_TYPE: str(modbus_client_type),
              CONF_PORT: str(modbus_client_port),
              CONF_MASTER_UNIT_ID: int(modbus_master_unit_id)}
    # type specific part
    if modbus_client_type == 'serial':
        config[CONF_METHOD] = DUCO_MODBUS_METHOD
        config[CONF_BAUDRATE] = DUCO_MODBUS_BAUD_RATE
        config[CONF_BYTESIZE] = DUCO_MODBUS_BYTE_SIZE
        config[CONF_STOPBITS] = DUCO_MODBUS_STOP_BITS
        config[CONF_PARITY] = DUCO_MODBUS_PARITY
    elif modbus_client_type == 'tcp':
        config[CONF_HOST] = 'ducobox.local'
    else:
        raise ValueError("modbus_client_type must be serial or tcp")

    return config


class DucoSystem(object):
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """

    def __init__(self, modbus_client_type, modbus_client_port,
                 modbus_master_unit_id=DUCO_MODBUS_MASTER_DEFAULT_UNIT_ID):
        """Initialize DucoSystem.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1 (str): Description of `param1`.
            param2 (:obj:`int`, optional): Description of `param2`. Multiple
                lines are supported.
            param3 (:obj:`list` of :obj:`str`): Description of `param3`.

        """
        self._config = create_config(modbus_client_type, modbus_client_port,
                                     modbus_master_unit_id)
        self.node_list = list()

    def __enter__(self):
        """Enter."""
        setup_modbus(self._config)
        self.node_list = enumerate_node_tree()
        return self

    def __exit__(self, exc_type, _exc_value, traceback):
        """Exit."""
        close_modbus()

    @property
    def config(self):
        """Return system configuration."""
        return self._config
