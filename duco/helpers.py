"""Helper functions."""

from duco.const import (DUCO_PCT_RANGE_START,
                        DUCO_PCT_RANGE_STEP,
                        DUCO_PCT_RANGE_STOP,
                        DUCO_REG_ADDR_NODE_ID_OFFSET)


def is_in_pct_range(value):
    """Return whether value is in duco percentage range."""
    return value in range(DUCO_PCT_RANGE_START,
                          DUCO_PCT_RANGE_STOP+DUCO_PCT_RANGE_STEP,
                          DUCO_PCT_RANGE_STEP)


def verify_in_pct_range(value):
    """Verify that value is in duco percentage range."""
    if not is_in_pct_range(value):
        raise ValueError("Value must be within {} and {} with steps of {}"
                         .format(DUCO_PCT_RANGE_START,
                                 DUCO_PCT_RANGE_STOP,
                                 DUCO_PCT_RANGE_STEP))


def to_register_addr(node_id, param_id):
    """Compute modbus address from node_id and param_id."""
    return node_id*DUCO_REG_ADDR_NODE_ID_OFFSET + param_id


def twos_comp(val, bits):
    """Compute the 2's complement of int value val."""
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set
        val = val - (1 << bits)         # compute negative value
    return val                          # return positive value as is
