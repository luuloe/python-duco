"""Test methods in duco/helpers.py."""
import unittest
import duco.helpers


class TestIsInPctRange(unittest.TestCase):
    """Class that tests to_register_addr function."""

    def test_true(self):
        self.assertTrue(duco.helpers.is_in_pct_range(0))
        self.assertTrue(duco.helpers.is_in_pct_range(100))
        for var in range(0, 105, 5):
            self.assertTrue(duco.helpers.is_in_pct_range(var))

    def test_false(self):
        self.assertFalse(duco.helpers.is_in_pct_range(-1))
        self.assertFalse(duco.helpers.is_in_pct_range(1))
        self.assertFalse(duco.helpers.is_in_pct_range(99))
        self.assertFalse(duco.helpers.is_in_pct_range(101))

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
