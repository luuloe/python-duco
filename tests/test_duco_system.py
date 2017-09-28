"""Test DucoSystem class."""
import unittest
import duco
from duco.const import (
    DUCO_MODULE_MASTER_DEFAULT_ADDRESS)


class TestConfig(unittest.TestCase):
    """Test the DucoSystem."""

    def test_master_address(self):
        """Test get_master_address returns the expected result."""
        dapi = duco.DucoSystem()
        # File created with create_file are empty
        self.assertEqual(DUCO_MODULE_MASTER_DEFAULT_ADDRESS,
                         dapi.get_master_address())

        dapi = duco.DucoSystem(7)
        # File created with create_file are empty
        self.assertEqual(7, dapi.get_master_address())
