"""Test methods in duco/duco.py."""


""" class TestProbeNodeId(unittest.TestCase):
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
        duco.modbus.MODBUSHUB.read_input_registers.assert_called_once() """


def test_duco():
    """Test duco dummy."""
    return True
