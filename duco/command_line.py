#! /usr/bin/python
"""Command line tool that wraps Python Duco."""
from duco.const import (__version__)


def main():
    """Main function."""
    print("python-duco version is " + __version__)


if __name__ == '__main__':
    main()
