#! /usr/bin/python
"""Command line tool that wraps Python Duco."""
import argparse
from duco.duco import (DucoSystem)

def parse_args():
    """Helper function for parsing arguments."""
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
    """Main function."""
    args = parse_args()
    
    dapi = DucoSystem(args.modbus_type, args.modbus_port)
    print(dapi.get_master_address())


if __name__ == '__main__':
    main()
