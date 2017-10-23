"""Duco nodes supported by python-duco."""
from duco.const import (DUCO_REG_ADDR_INPUT_STATUS,
                        DUCO_REG_ADDR_INPUT_FAN_ACTUAL,
                        DUCO_REG_ADDR_INPUT_TEMPERATURE,
                        DUCO_REG_ADDR_INPUT_CO2_ACTUAL,
                        DUCO_REG_ADDR_INPUT_RH_ACTUAL,
                        DUCO_REG_ADDR_INPUT_GROUP,
                        DUCO_REG_ADDR_HOLD_FAN_SETPOINT,
                        DUCO_REG_ADDR_HOLD_CO2_SETPOINT,
                        DUCO_REG_ADDR_HOLD_RH_SETPOINT,
                        DUCO_REG_ADDR_HOLD_RH_DELTA,
                        DUCO_REG_ADDR_HOLD_FLOW,
                        DUCO_REG_ADDR_HOLD_AUTOMIN,
                        DUCO_REG_ADDR_HOLD_AUTOMAX,
                        DUCO_REG_ADDR_HOLD_ACTION,
                        DUCO_REG_ADDR_HOLD_BUTTON_1,
                        DUCO_REG_ADDR_HOLD_BUTTON_2,
                        DUCO_REG_ADDR_HOLD_BUTTON_3,
                        DUCO_REG_ADDR_HOLD_MANUAL_TIME,
                        DUCO_TEMPERATURE_SCALE_FACTOR,
                        DUCO_TEMPERATURE_PRECISION,
                        DUCO_RH_SCALE_FACTOR,
                        DUCO_RH_PRECISION,
                        DUCO_ZONE_STATUS_OFFSET,
                        DUCO_ACTION_OFFSET)
from duco.enum_types import (ModuleType, ZoneStatus, ZoneAction)
from duco.modbus import (REGISTER_TYPE_INPUT, REGISTER_TYPE_HOLDING,
                         DATA_TYPE_INT, to_register_addr,
                         probe_node_id, ModbusRegister)


def enumerate_node_tree():
    """Enumerate Duco module tree."""
    node_id = 1
    node_found = True
    node_list = []

    while node_found:
        node_type = probe_node_id(node_id)

        if node_type is False:
            node_found = False
        else:
            node_list.append(Node.factory(node_id, node_type))

        node_id = node_id + 1

    return node_list


class Node(object):
    """Duco base node."""

    # Create based on ModuleType:
    @staticmethod
    def factory(node_id, node_type):
        """Create Node based on node_id and node_type."""
        if node_type == ModuleType.MASTER:
            return BoxNode(node_id, node_type)
        elif node_type == ModuleType.VALVE_SENSORLESS:
            return SensorlessValveNode(node_id, node_type)
        elif node_type == ModuleType.VALVE_CO2:
            return CO2ValveNode(node_id, node_type)
        elif node_type == ModuleType.VALVE_RH:
            return RHValveNode(node_id, node_type)
        elif node_type == ModuleType.USER_CONTROLLER:
            return UserControllerNode(node_id, node_type)
        elif node_type == ModuleType.ROOM_SENSOR_CO2:
            return CO2SensorNode(node_id, node_type)
        elif node_type == ModuleType.ROOM_SENSOR_RH:
            return RHSensorNode(node_id, node_type)
        assert 0, "ModuleType not implemented: " + ModuleType(node_type)

    def __init__(self, node_id, node_type):
        """Initialize Node base."""
        self._node_id = int(node_id)
        self._node_type = ModuleType(node_type)
        self._child_nodes = []
        # registers
        # name, register, register_type,
        # unit_of_measurement, count, scale, offset, data_type, precision
        # input
        self._reg_status = ModbusRegister(
            'Zone status',
            to_register_addr(self._node_id, DUCO_REG_ADDR_INPUT_STATUS),
            REGISTER_TYPE_INPUT, '', 1, 1,
            DUCO_ZONE_STATUS_OFFSET, DATA_TYPE_INT, 0)

        self._reg_fan_actual = ModbusRegister(
            'Fan actual',
            to_register_addr(self._node_id, DUCO_REG_ADDR_INPUT_FAN_ACTUAL),
            REGISTER_TYPE_INPUT, '%', 1, 1, 0, DATA_TYPE_INT, 0)

        self._reg_zone = ModbusRegister(
            'Zone',
            to_register_addr(self._node_id, DUCO_REG_ADDR_INPUT_GROUP),
            REGISTER_TYPE_INPUT, '', 1, 1, 0, DATA_TYPE_INT, 0)
        # holding
        self._reg_setpoint = ModbusRegister(
            'Zone setpoint',
            to_register_addr(self._node_id, DUCO_REG_ADDR_HOLD_FAN_SETPOINT),
            REGISTER_TYPE_HOLDING, '%', 1, 1, 0, DATA_TYPE_INT, 0)

        self._reg_action = ModbusRegister(
            'Zone action',
            to_register_addr(self._node_id, DUCO_REG_ADDR_HOLD_ACTION),
            REGISTER_TYPE_HOLDING, '', 1, 1,
            DUCO_ACTION_OFFSET, DATA_TYPE_INT, 0)

    @property
    def node_id(self):
        """Return the id of the node."""
        return self._node_id

    @property
    def node_type(self):
        """Return the type of the node."""
        return self._node_type

    @property
    def action(self):
        """Return the zone action of the node."""
        # synchronous update for now
        self._reg_action.update()
        return ZoneAction(self._reg_action.value)

    @property
    def status(self):
        """Return the zone status of the node."""
        # synchronous update for now
        print(list(ZoneStatus))
        self._reg_status.update()
        return ZoneStatus(self._reg_status.value)

    @property
    def zone(self):
        """Return the zone to which the node belongs."""
        # synchronous update for now
        self._reg_zone.update()
        return self._reg_zone.value

    def state(self):
        """Return the state of the node."""
        return (self._reg_action.state, self._reg_status.state,
                self._reg_zone.state)


class AutoMinMaxCapable(object):
    """Duco node containing AutoMin and AutoMax registers."""

    def __init__(self, node_id):
        """Initialize AutoMinMaxCapable."""
        self._reg_automin = ModbusRegister(
            'AutoMin',
            to_register_addr(node_id, DUCO_REG_ADDR_HOLD_AUTOMIN),
            REGISTER_TYPE_HOLDING, '%', 1, 1, 0, DATA_TYPE_INT, 0)

        self._reg_automax = ModbusRegister(
            'AutoMax',
            to_register_addr(node_id, DUCO_REG_ADDR_HOLD_AUTOMAX),
            REGISTER_TYPE_HOLDING, '%', 1, 1, 0, DATA_TYPE_INT, 0)

    @property
    def auto_min(self):
        """Return the auto min of the node."""
        # synchronous update for now
        self._reg_automin.update()
        return self._reg_automin.value

    @property
    def auto_max(self):
        """Return the auto max of the node."""
        # synchronous update for now
        self._reg_automax.update()
        return self._reg_automax.value

    def state(self):
        """Return the state of the node as a tuple."""
        return (self._reg_automin.state, self._reg_automax.state)


class BoxNode(Node, AutoMinMaxCapable):
    """Duco box node."""

    def __init__(self, node_id, node_type):
        """Initialize BoxNode node."""
        Node.__init__(self, node_id, node_type)
        AutoMinMaxCapable.__init__(self, node_id)
        # no additional registers

    def state(self):
        """Return the state of the node as a tuple."""
        return Node.state(self) + AutoMinMaxCapable.state(self)


class TemperatureSensor(object):
    """TemperatureSensor base class."""

    def __init__(self, node_id):
        """Initialize TemperatureSensor base class."""
        # input
        self._reg_temperature = ModbusRegister(
            'Temperature',
            to_register_addr(node_id, DUCO_REG_ADDR_INPUT_TEMPERATURE),
            REGISTER_TYPE_INPUT, '°C', 1, DUCO_TEMPERATURE_SCALE_FACTOR,
            0, DATA_TYPE_INT, DUCO_TEMPERATURE_PRECISION)

    @property
    def temperature(self):
        """Return the measured indoor air temperature."""
        # synchronous update for now
        self._reg_temperature.update()
        return self._reg_temperature.value

    def state(self):
        """Return the state of the node as a tuple."""
        return (self._reg_temperature.state,)


class Valve(Node, AutoMinMaxCapable, TemperatureSensor):
    """Valve base class."""

    def __init__(self, node_id, node_type):
        """Initialize Valve base class."""
        Node.__init__(self, node_id, node_type)
        AutoMinMaxCapable.__init__(self, node_id)
        TemperatureSensor.__init__(self, node_id)

        # holding
        self._reg_flow = ModbusRegister(
            'Flow',
            to_register_addr(self._node_id, DUCO_REG_ADDR_HOLD_FLOW),
            REGISTER_TYPE_HOLDING, 'm3/h', 1, 1, 0, DATA_TYPE_INT, 0)
        # holding

    @property
    def flow(self):
        """Return the configured valve flow."""
        # synchronous update for now
        self._reg_flow.update()
        return self._reg_flow.value

    def state(self):
        """Return the state of the node as a tuple."""
        return (Node.state(self), AutoMinMaxCapable.state(self),
                TemperatureSensor.state(self), self._reg_flow.state)


class CO2Sensor(object):
    """CO2Sensor base class."""

    def __init__(self, node_id):
        """Initialize CO2Sensor base class."""
        # input
        self._reg_co2_value = ModbusRegister(
            'CO2 value',
            to_register_addr(node_id, DUCO_REG_ADDR_INPUT_CO2_ACTUAL),
            REGISTER_TYPE_INPUT, 'ppm', 1, 1,
            0, DATA_TYPE_INT, 0)
        # holding
        self._reg_co2_setpoint = ModbusRegister(
            'CO2 setpoint',
            to_register_addr(node_id, DUCO_REG_ADDR_HOLD_CO2_SETPOINT),
            REGISTER_TYPE_HOLDING, 'ppm', 1, 1,
            0, DATA_TYPE_INT, 0)

    @property
    def co2_value(self):
        """Return the measured CO2 concentration in ppm."""
        # synchronous update for now
        self._reg_co2_value.update()
        return self._reg_co2_value.value

    @property
    def co2_setpoint(self):
        """Return the desired CO2 concentration in ppm."""
        # synchronous update for now
        self._reg_co2_setpoint.update()
        return self._reg_co2_setpoint.value

    def state(self):
        """Return the state of the node as a tuple."""
        return (self._reg_co2_setpoint.state, self._reg_co2_value.state)


class RHSensor(object):
    """RHSensor base class."""

    def __init__(self, node_id):
        """Initialize RHSensor base class."""
        # input
        self._reg_rh_value = ModbusRegister(
            'RH value',
            to_register_addr(node_id, DUCO_REG_ADDR_INPUT_RH_ACTUAL),
            REGISTER_TYPE_INPUT, '%', 1, DUCO_RH_SCALE_FACTOR,
            0, DATA_TYPE_INT, DUCO_RH_PRECISION)
        # holding
        self._reg_rh_setpoint = ModbusRegister(
            'RH setpoint',
            to_register_addr(node_id, DUCO_REG_ADDR_HOLD_RH_SETPOINT),
            REGISTER_TYPE_HOLDING, '%', 1, 1,
            0, DATA_TYPE_INT, 0)
        self._reg_rh_delta = ModbusRegister(
            'RH delta',
            to_register_addr(node_id, DUCO_REG_ADDR_HOLD_RH_DELTA),
            REGISTER_TYPE_HOLDING, '-', 1, 1,
            0, DATA_TYPE_INT, 0)

    @property
    def rh_value(self):
        """Return the measured relative humidity in %."""
        # synchronous update for now
        self._reg_rh_value.update()
        return self._reg_rh_value.value

    @property
    def rh_setpoint(self):
        """Return the desired relative humidity in %."""
        # synchronous update for now
        self._reg_rh_setpoint.update()
        return self._reg_rh_setpoint.value

    @property
    def is_rh_delta_enabled(self):
        """Return whether or not RH delta control is activated."""
        # synchronous update for now
        self._reg_rh_delta.update()
        return bool(self._reg_rh_delta.value)

    def state(self):
        """Return the state of the node as a tuple."""
        return (self._reg_rh_setpoint.state, self._reg_rh_value.state,
                self._reg_rh_delta.state)


class UserController(object):
    """UserController base class."""

    def __init__(self, node_id):
        """Initialize UserController base class."""
        # holding
        self._reg_button_1 = ModbusRegister(
            'Button 1',
            to_register_addr(node_id, DUCO_REG_ADDR_HOLD_BUTTON_1),
            REGISTER_TYPE_HOLDING, '%', 1, 1,
            0, DATA_TYPE_INT, 0)
        self._reg_button_2 = ModbusRegister(
            'Button 2',
            to_register_addr(node_id, DUCO_REG_ADDR_HOLD_BUTTON_2),
            REGISTER_TYPE_HOLDING, '%', 1, 1,
            0, DATA_TYPE_INT, 0)
        self._reg_button_3 = ModbusRegister(
            'Button 3',
            to_register_addr(node_id, DUCO_REG_ADDR_HOLD_BUTTON_3),
            REGISTER_TYPE_HOLDING, '%', 1, 1,
            0, DATA_TYPE_INT, 0)
        self._reg_manual_time = ModbusRegister(
            'Manual time',
            to_register_addr(node_id, DUCO_REG_ADDR_HOLD_MANUAL_TIME),
            REGISTER_TYPE_HOLDING, 'minutes', 1, 1,
            0, DATA_TYPE_INT, 0)

    @property
    def button1(self):
        """Return the current setpoint behind button 1."""
        # synchronous update for now
        self._reg_button_1.update()
        return self._reg_button_1.value

    @property
    def button2(self):
        """Return the current setpoint behind button 2."""
        # synchronous update for now
        self._reg_button_2.update()
        return self._reg_button_2.value

    @property
    def button3(self):
        """Return the current setpoint behind button 3."""
        # synchronous update for now
        self._reg_button_3.update()
        return self._reg_button_3.value

    @property
    def manual_time(self):
        """Return the duration of the manual mode."""
        # synchronous update for now
        self._reg_manual_time.update()
        return self._reg_manual_time.value

    def state(self):
        """Return the state of the node as a tuple."""
        return (self._reg_button_1.state, self._reg_button_2.state,
                self._reg_button_3.state, self._reg_manual_time.state)


class SensorlessValveNode(Valve):
    """Valve base class."""

    def __init__(self, node_id, node_type):
        """Initialize Valve base class."""
        Valve.__init__(self, node_id, node_type)


class CO2ValveNode(Valve, CO2Sensor):
    """CO2ValveNode class."""

    def __init__(self, node_id, node_type):
        """Initialize CO2ValveNode."""
        Valve.__init__(self, node_id, node_type)
        CO2Sensor.__init__(self, node_id)

    def state(self):
        """Return the state of the node as a tuple."""
        return Valve.state(self) + CO2Sensor.state(self)


class RHValveNode(Valve, RHSensor):
    """RHValveNode class."""

    def __init__(self, node_id, node_type):
        """Initialize RHValveNode."""
        Valve.__init__(self, node_id, node_type)
        RHSensor.__init__(self, node_id)

    def state(self):
        """Return the state of the node as a tuple."""
        return Valve.state(self) + RHSensor.state(self)


class UserControllerNode(Node, UserController):
    """UserControllerNode class."""

    def __init__(self, node_id, node_type):
        """Initialize UserControllerNode."""
        Node.__init__(self, node_id, node_type)
        UserController.__init__(self, node_id)

    def state(self):
        """Return the state of the node as a tuple."""
        return Node.state(self) + UserController.state(self)


class CO2SensorNode(Node, UserController, CO2Sensor):
    """CO2SensorNode class."""

    def __init__(self, node_id, node_type):
        """Initialize CO2SensorNode."""
        Node.__init__(self, node_id, node_type)
        UserController.__init__(self, node_id)
        CO2Sensor.__init__(self, node_id)

    def state(self):
        """Return the state of the node as a tuple."""
        state = Node.state(self) + UserController.state(self)
        return state + CO2Sensor.state(self)


class RHSensorNode(Node, UserController, RHSensor):
    """RHSensorNode class."""

    def __init__(self, node_id, node_type):
        """Initialize RHSensorNode."""
        Node.__init__(self, node_id, node_type)
        UserController.__init__(self, node_id)
        RHSensor.__init__(self, node_id)

    def state(self):
        """Return the state of the node as a tuple."""
        state = Node.state(self) + UserController.state(self)
        return state + RHSensor.state(self)
