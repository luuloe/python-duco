"""Helper functions."""

from duco.const import (
    DUCO_REG_ADDR_NODE_ID_OFFSET
)


def verify_value_in_range(value, range_start, range_step, range_stop):
    """Verify that value is in range _start,_step,_stop."""
    if value not in range(range_start,
                          range_stop+range_step,
                          range_step):
        raise ValueError("Value must be within {} and {} with steps of {}"
                         .format(range_start,
                                 range_stop,
                                 range_step))


def to_register_addr(node_id, param_id):
    """Compute modbus address from node_id and param_id."""
    return node_id*DUCO_REG_ADDR_NODE_ID_OFFSET + param_id


def twos_comp(val, bits):
    """Compute the 2's complement of int value val."""
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set
        val = val - (1 << bits)         # compute negative value
    return val                          # return positive value as is
