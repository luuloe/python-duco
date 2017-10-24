python-duco |Build Status| |Coverage Status| |Doc Status| |Codacy Status| |Coverity Status|
=============================================================
Python API and command line tool for communicating to the Duco™ Ventilation System. 

The Duco™ Ventilation System supports the option for an external unit to communicate via the ModBus interface. A Duco™ 'master' with ModBus interface (e.g. DucoBox Focus or IQ-unit) exposes all information of the Duco-network and allows external units to control the Duco-network and change settings over ModBus.

python-duco is based on publicly available documentation of the Ducobox and ModBus interface.

Features
============
* Communication via ModBus RTU and ModBus TCP
* Automatic discovery of Duco-network topology 
* Provide read and write access to all modules in Duco-network (master, valves, sensors, ...)
* Synchronous API
* Caching of module information and settings, ModBus access via asynchronous queue

Status
============
The project is currently in alpha status and not ready for integration.

Installation
============

.. code-block:: bash

    [sudo] pip install python-duco

Usage
=====

Module
------
You can import the module as `duco`.

.. code-block:: python

    import duco
    
    with DucoSystem(args.modbus_type, args.modbus_port) as dapi:
        for node in dapi.node_list:
            print(node.node_type)
            print(node.state())

Contributing
=====
Just fork the repo and raise your PR against dev branch.

License Information
=====
Python-duco is not developed by Duco™ and therefore has no affiliation with Duco™. As a result no support can be claimed from Duco™.

Released under the MIT License.

.. |Build Status| image:: https://travis-ci.org/luuloe/python-duco.svg?branch=master
   :target: https://travis-ci.org/luuloe/python-duco
.. |Coverage Status| image:: https://coveralls.io/repos/github/luuloe/python-duco/badge.svg?branch=master
   :target: https://coveralls.io/github/luuloe/python-duco?branch=master
.. |Doc Status| image:: https://readthedocs.org/projects/python-duco/badge/?version=latest
   :target: http://python-duco.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |Coverity Status| image:: https://scan.coverity.com/projects/14019/badge.svg
   :target: https://scan.coverity.com/projects/luuloe-mbusd
   :alt: Coverity Scan Build Status
.. |Codacy Status| image:: https://api.codacy.com/project/badge/Grade/629d143e73c842d69b994efa4e259e77
   :target: https://www.codacy.com/app/luuloe/python-duco?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=luuloe/python-duco&amp;utm_campaign=Badge_Grade
   :alt: Codacy Status
