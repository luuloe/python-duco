"""Test methods in duco/helpers.py."""
import unittest
import duco.helpers


class TestVerifyValueInRange(unittest.TestCase):
    """Class that tests verify_value_in_range function."""

    def test_is_none(self):
        self.assertIsNone(duco.helpers.verify_value_in_range(0, 0, 5, 100))
        self.assertIsNone(duco.helpers.verify_value_in_range(100, 0, 5, 100))
        for var in range(0, 105, 5):
            self.assertIsNone(duco.helpers.verify_value_in_range(var, 0, 5, 100))

    def test_raises(self):
        self.assertRaises(ValueError, lambda: duco.helpers.verify_value_in_range(-1, 0, 5, 100))
        self.assertRaises(ValueError, lambda: duco.helpers.verify_value_in_range(1, 0, 5, 100))
        self.assertRaises(ValueError, lambda: duco.helpers.verify_value_in_range(99, 0, 5, 100))
        self.assertRaises(ValueError, lambda: duco.helpers.verify_value_in_range(101, 0, 5, 100))

class TestToRegisterAddress(unittest.TestCase):
    """Class that tests to_register_addr function."""

    def test_1(self):
        node_id = 3
        param_id = 5
        self.assertEqual(duco.helpers.to_register_addr(node_id, param_id),
                         (node_id*10+param_id))

    def test_2(self):
        node_id = 9
        param_id = 8
        self.assertEqual(duco.helpers.to_register_addr(node_id, param_id),
                         (node_id*10+param_id))
