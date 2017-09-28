Python Duco |Build Status| |Coverage Status| |Doc Status|
=============================================================
Python API and command line tool for communicating to the Duco™ Ventilation System. 

The Duco™ Ventilation System supports the option for an external unit to communicate via the ModBus interface. A Duco™ 'master' with ModBus interface (e.g. DucoBox Focus or IQ-unit) exposes all information of the Duco-network and allows external units to control the Duco-network and change settings over ModBus.

Features
============
* Automatic discovery of Duco-network topology via ModBus 
* Provide read and write access to all modules in Duco-network (master, valves, sensors, etc.)
* Supports ModBus RTU (feasibility for TCP via ModBus TCP gateway to be determined)
* Synchronous API
* Caching of module information and settings, ModBus access via asynchronous queue

Status
============
The project is currently in alpha status and not ready for use.

Release scope: 
1. Setting up the project: 
-- * Repository structure 
   * Hello world like public API
   * Automatic code analysis via flak8 and pylint
   * Testing with Tox
   * Travis CI integration, lint and Tox targets
   * Sphinx documentation generation
   * ReadTheDocs integration 
   * Release strategy: PyPI package generation
2. First functionality:
-- * Duco-network constants and object structure
   * Finalize DucoSystem public API
   * Setup ModBus simulator
   * ModBus communication for Duco master module

Installation
============

.. code-block:: bash

    [sudo] pip install python-duco

Usage
=====

Module
------

You can import the module as `duco`.

   code-block:: python

    import duco

.. |Build Status| image:: https://travis-ci.org/luuloe/python-duco.svg?branch=master
   :target: https://travis-ci.org/luuloe/python-duco
.. |Coverage Status| image:: https://coveralls.io/repos/github/luuloe/python-duco/badge.svg?branch=master
   :target: https://coveralls.io/github/luuloe/python-duco?branch=master
.. |Doc Status| image:: https://readthedocs.org/projects/python-duco/badge/?version=latest
   :target: http://python-duco.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
