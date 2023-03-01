.. role:: framework

.. _software_framework:

Software Framework and Limitations
==================================

The project has a lot of software components, and it is important to understand how they fit together.
This section describes the software framework and the limitations of the current implementation.

The project is written in Python and contains a number of sub-modules, listed in :ref:`table-project-modules`.
Each module contains classes, methods and functions.

.. only:: html

   See :ref:`api-documentation` for more information on the code structure.

.. _table-project-modules:
.. table:: Project modules

    +-------------------------------------------------+----------------------------------------------------------------------------------------------+
    | Module                                          | Description                                                                                  |
    +=================================================+==============================================================================================+
    | :class:`~.network.Network`                      | Network Class contains methods to create the simulation environment and extract              |
    |                                                 | data from the environment.                                                                   |
    +-------------------------------------------------+----------------------------------------------------------------------------------------------+
    | :class:`~.agent.Agent`                          | Agent Class                                                                                  |
    |                                                 |                                                                                              |
    +-------------------------------------------------+----------------------------------------------------------------------------------------------+
