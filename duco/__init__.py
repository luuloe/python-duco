"""Init file for Python Duco."""
from .const import DUCO_MODBUS_DEFAULT_MASTER_ADDRESS
from .duco import DucoSystem

__all__ = (
    'DUCO_MODBUS_DEFAULT_MASTER_ADDRESS',
    'DucoSystem'
)
