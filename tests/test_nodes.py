"""Test methods in duco/nodes.py."""
import unittest
# from unittest.mock import Mock
from unittest.mock import MagicMock, Mock, PropertyMock, patch
from duco.const import (
    DUCO_ACTION_OFFSET,
    DUCO_REG_ADDR_INPUT_FAN_ACTUAL,
    DUCO_REG_ADDR_INPUT_GROUP,
    DUCO_REG_ADDR_INPUT_STATUS,
    DUCO_REG_ADDR_HOLD_ACTION,
    DUCO_ZONE_STATUS_OFFSET
)
from duco.helpers import (to_register_addr)
from duco.enum_types import (
    ModuleType, ZoneAction, ZoneStatus
)
import duco.modbus
import duco.nodes


class TestNode(unittest.TestCase):
    def test_factory(self):
        node_id = 23
        hub = MagicMock(spec=['read_holding_registers', 'read_input_registers', 'write_register'])

        type_dict = {ModuleType.MASTER: duco.nodes.BoxNode(node_id, ModuleType.MASTER, hub),
                     ModuleType.VALVE_SENSORLESS: duco.nodes.SensorlessValveNode(node_id, ModuleType.VALVE_SENSORLESS, hub),
                     ModuleType.VALVE_CO2: duco.nodes.CO2ValveNode(node_id, ModuleType.VALVE_CO2, hub),
                     ModuleType.VALVE_RH: duco.nodes.RHValveNode(node_id, ModuleType.VALVE_RH, hub),
                     ModuleType.USER_CONTROLLER: duco.nodes.UserControllerNode(node_id, ModuleType.USER_CONTROLLER, hub),
                     ModuleType.ROOM_SENSOR_CO2: duco.nodes.CO2SensorNode(node_id, ModuleType.ROOM_SENSOR_CO2, hub),
                     ModuleType.ROOM_SENSOR_RH: duco.nodes.RHSensorNode(node_id, ModuleType.ROOM_SENSOR_RH, hub)}

        # non-happy flow
        with self.assertRaises(ValueError): duco.nodes.Node.factory(node_id, 21, hub)
        hub.assert_not_called()

        #for module_type in ModuleType: ! not all ModuleTypes implemented
        for node_type in type_dict:
            node = duco.nodes.Node.factory(node_id, node_type, hub)

            self.assertIs(type(node), type(type_dict[node_type]))
            self.assertEqual(node.node_id, node_id, "")
            self.assertEqual(node.node_type, node_type, "")

    def test_init(self):
        node_id = 1
        hub = MagicMock(spec=['read_holding_registers', 'read_input_registers', 'write_register'])
        hub_read_result_ok = MagicMock(spec=['registers'])

        nodes = [duco.nodes.BoxNode(node_id, ModuleType.MASTER, hub),
                 duco.nodes.SensorlessValveNode(node_id, ModuleType.VALVE_SENSORLESS, hub),
                 duco.nodes.CO2ValveNode(node_id, ModuleType.VALVE_CO2, hub),
                 duco.nodes.RHValveNode(node_id, ModuleType.VALVE_RH, hub),
                 duco.nodes.UserControllerNode(node_id, ModuleType.USER_CONTROLLER, hub),
                 duco.nodes.CO2SensorNode(node_id, ModuleType.ROOM_SENSOR_CO2, hub),
                 duco.nodes.RHSensorNode(node_id, ModuleType.ROOM_SENSOR_RH, hub)]

        for node in nodes:
            # node_id.get
            self.assertEqual(node.node_id, node_id, "")
            # action.get
            self.assertEqual(node.action, None, "")
            # action.set
            for action in ZoneAction:
                node.action = action
                hub.write_register.assert_called_with(to_register_addr(node_id, DUCO_REG_ADDR_HOLD_ACTION), action-DUCO_ACTION_OFFSET)

            with self.assertRaises(ValueError): node.action = -1
            with self.assertRaises(ValueError): node.action = 7
            # fan_actual.get
            fan_actual_ref = 42
            registers = PropertyMock(return_value=[fan_actual_ref])
            type(hub_read_result_ok).registers = registers
            hub.read_input_registers.return_value = hub_read_result_ok

            self.assertEqual(node.fan_actual, str(fan_actual_ref))
            hub.read_input_registers.assert_called_with(to_register_addr(node_id, DUCO_REG_ADDR_INPUT_FAN_ACTUAL), 1)
            # status.get
            for status in ZoneStatus:
                registers = PropertyMock(return_value=[status-DUCO_ZONE_STATUS_OFFSET])
                type(hub_read_result_ok).registers = registers
                hub.read_input_registers.return_value = hub_read_result_ok

                self.assertEqual(node.status, status, "")
                hub.read_input_registers.assert_called_with(to_register_addr(node_id, DUCO_REG_ADDR_INPUT_STATUS), 1)
            # zone.get
            zone_ref = 2
            registers = PropertyMock(return_value=[zone_ref])
            type(hub_read_result_ok).registers = registers
            hub.read_input_registers.return_value = hub_read_result_ok

            self.assertEqual(node.zone, str(zone_ref))
            hub.read_input_registers.assert_called_with(to_register_addr(node_id, DUCO_REG_ADDR_INPUT_GROUP), 1)



class TestBoxNode(unittest.TestCase):
    def test_init(self):
        self.assertTrue(True)


class TestSensorlessValveNode(unittest.TestCase):
    def test_init(self):
        self.assertTrue(True)


class TestCO2ValveNode(unittest.TestCase):
    def test_init(self):
        self.assertTrue(True)


class TestRHValveNode(unittest.TestCase):
    def test_init(self):
        self.assertTrue(True)


class TestUserControllerNode(unittest.TestCase):
    def test_init(self):
        self.assertTrue(True)


class TestCO2SensorNode(unittest.TestCase):
    def test_init(self):
        self.assertTrue(True)


class TestRHSensorNode(unittest.TestCase):
    def test_all(self):
        node_id = 1
        hub = MagicMock(spec=['read_holding_registers', 'read_input_registers', 'write_register'])
        hub_read_result_ok = MagicMock(spec=['registers'])
        
        rh_ref = 4974
        registers = PropertyMock(return_value=[rh_ref])
        type(hub_read_result_ok).registers = registers
        hub.read_input_registers.return_value = hub_read_result_ok

        rh_sensor = duco.nodes.RHSensorNode(node_id, ModuleType.ROOM_SENSOR_RH, hub)
        #print(str(rh_sensor))
        #print(rh_sensor.state)
        self.assertTrue(True)

