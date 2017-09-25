"""Duco."""
from duco.const import (
    DUCO_MODULE_MASTER_DEFAULT_ADDRESS, __version__)

class DucoSystem(object):
    def __init__(self, box_address=1):
        self.box_address = box_address