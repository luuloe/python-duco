"""Duco."""
import logging

from duco.const import (
    PROJECT_PACKAGE_NAME, DUCO_REG_ADDR_INPUT_MODULE_TYPE,
    DUCO_MODBUS_MASTER_DEFAULT_UNIT_ID)

from duco.enum_types import (ModuleType)
from duco.modbus import (create_client_config, ModbusHub)
from duco.nodes import (to_register_addr, Node)

_LOGGER = logging.getLogger(PROJECT_PACKAGE_NAME)


class DucoBox:
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
                 modbus_client_host=None,
                 modbus_master_unit_id=DUCO_MODBUS_MASTER_DEFAULT_UNIT_ID):
        """Initialize DucoBox.

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
        client_config = create_client_config(modbus_client_type,
                                             modbus_client_port,
                                             modbus_client_host,
                                             modbus_master_unit_id)
        self._modbus_hub = ModbusHub(client_config)
        self.node_list = list()

    def __enter__(self):
        """Enter."""
        self._modbus_hub.setup()
        self.__enumerate_node_tree()
        return self

    def __exit__(self, exc_type, _exc_value, traceback):
        """Exit."""
        self._modbus_hub.close()

    def __enumerate_node_tree(self):
        """Enumerate Duco node tree."""
        node_id = 1
        node_found = True
        self.node_list = list()

        while node_found:
            node_type = self.__probe_node_id(node_id)

            if node_type is False:
                node_found = False
            else:
                self.node_list.append(
                    Node.factory(node_id, node_type, self._modbus_hub))

            node_id = node_id + 1

    def __probe_node_id(self, node_id):
        """Probe Modbus for node_id module type."""
        _LOGGER.debug("probe node_id %d", node_id)
        modbus_result = self._modbus_hub.read_input_registers(
            to_register_addr(node_id, DUCO_REG_ADDR_INPUT_MODULE_TYPE), 1)
        try:
            register = modbus_result.registers
            response = register[0]
        except AttributeError:
            _LOGGER.debug("No response from node_id %d", node_id)
            return False

        if ModuleType.supported(response):
            module_type = ModuleType(response)
            _LOGGER.debug("node_id %d is a module of type %s",
                          node_id, module_type)
            return module_type

        return False
