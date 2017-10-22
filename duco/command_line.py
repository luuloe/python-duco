#! /usr/bin/python
"""Command line tool that wraps Python Duco."""
import logging
import argparse
from duco.const import (PROJECT_PACKAGE_NAME)
from duco.duco import (DucoSystem)


_LOGGER = logging.getLogger(PROJECT_PACKAGE_NAME)


def configure_logging():
    """Configure logging for command line."""
    _LOGGER.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to console
    console.setFormatter(formatter)

    # add console to logger
    _LOGGER.addHandler(console)


def parse_args():
    """Parse command line arguments."""
    description = 'Command line interface to Duco Ventilation System'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--type', dest='modbus_type',
                        default='serial', help='modbus client type; '
                        'supported: serial, tcp')

    parser.add_argument('--port', dest='modbus_port',
                        help='modbus client port ')

    parser.add_argument('--host', dest='modbus_tcp_host',
                        default='localhost',
                        help='optional, modbus tcp host')

    return parser.parse_args()


def main():
    """Execute main function."""
    args = parse_args()

    configure_logging()

    with DucoSystem(args.modbus_type, args.modbus_port) as dapi:
        for node in dapi.node_list:
            print(node.node_type)
            print(node.state())


if __name__ == '__main__':
    main()
