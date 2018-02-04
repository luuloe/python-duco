"""Test methods in duco/modbus.py."""
from duco.const import (DUCO_MODULE_TYPE_MASTER,
                        DUCO_MODULE_TYPE_ACTUATOR_PRINT)
from duco.enum_types import (ModuleType)
import unittest


class TestModuleType(unittest.TestCase):
    def test_supported(self):
        for x in range(DUCO_MODULE_TYPE_MASTER, 10):
            self.assertTrue(ModuleType.supported(x), "msg")

        self.assertFalse(ModuleType.supported(DUCO_MODULE_TYPE_MASTER-1), "")
        self.assertFalse(ModuleType.supported(
            DUCO_MODULE_TYPE_ACTUATOR_PRINT+1), "")
