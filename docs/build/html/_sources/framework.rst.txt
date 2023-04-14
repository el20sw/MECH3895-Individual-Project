.. role:: framework

.. _software_framework:

Software Framework
==================

The project has a lot of software components, and it is important to understand how they fit together.
This section describes the software framework of the project.

The project is written in Python and contains a number of sub-modules, listed in :ref:`table-project-modules`.
Each module contains classes, methods and functions.

.. only:: html

   See :doc:`api` for more information on the code structure.

.. _table-project-modules:
.. table:: Project modules

    +-------------------------------------------------+----------------------------------------------------------------------------------------------+
    | Module                                          | Description                                                                                  |
    +=================================================+==============================================================================================+
    | :class:`~.network.Network`                      | Network Class contains methods to create the simulation environment and extract              |
    |                                                 | data from the environment.                                                                   |
    +-------------------------------------------------+----------------------------------------------------------------------------------------------+
    | :class:`~.agent.Agent`                          | Agent Class contains methods to control, move and get data from the Agents in the simulation.|
    |                                                 |                                                                                              |
    +-------------------------------------------------+----------------------------------------------------------------------------------------------+
    | :mod:`~.communication`                          | Communication Module contains functions to handle Agent-Agent communication.                 |
    |                                                 |                                                                                              |
    +-------------------------------------------------+----------------------------------------------------------------------------------------------+
    | :mod:`~.simulation`                             | Simulation Module contains functionality for running and configuring a simulation.           |
    |                                                 |                                                                                              |
    +-------------------------------------------------+----------------------------------------------------------------------------------------------+
    | :mod:`~.agent_generator`                        | Agent Generator Module contains functionality for generating Agents for the simulation with  |
    |                                                 | the desired configuration.                                                                   |
    +-------------------------------------------------+----------------------------------------------------------------------------------------------+
    | :mod:`~.render`                                 | Render Module contains functionality for graphically displaying the agents and environment   |
    |                                                 | in the simulation as an animation.                                                           |
    +-------------------------------------------------+----------------------------------------------------------------------------------------------+


Project Structure
-----------------

The entrance point of the project is the :file:`main.py` file. This file contains functions to create and run a simulation.

For a more custom simulation, a number of classes and functions can be used to create a simulation. The file :file:`main.py` 
contains examples of how to use these classes and functions and how they work together to create a simulation and get results.

Overview of each component of the project is given below.

.. _software_framework_network:

Network Class
-------------

The :class:`~.network.Network` class contains methods to create the simulation environment and extract data from the environment.
The class is instantiated in the :class:`~.simulation.Simulation` class, and is used to create the environment Agents operate in.

Example networks can be found in the :file:`networks` folder. Custom networks can be created though they have to
be an EPANET network file, of the type .inp.

Once a network is created by initialising the :class:`~.network.Network` class, it can be passed to the :class:`~.simulation.Simulation` class
or simply used to extract key data such as the number of pipes and junctions in the network.

.. The :class:`~.network.Network` class contains the following methods:

.. .. currentmodule:: src.network

.. ====================  ============================================================================================================
.. Method                 Description
.. ====================  ============================================================================================================
.. :func:`__init__`       Creates a Network object.
.. :func:`to_graph`       Creates an undirected NetworkX graph from the Network object.
.. :func:`get_nodes`      Returns a list of all nodes in the Network.
.. ====================  ============================================================================================================

.. _software_framework_agent:

Agent Class
-----------

The :class:`~.agent.Agent` class contains methods to control, move and get data from the Agents in the simulation.
The class is instantiated in the :class:`~.agent_generator.AgentGenerator` class, and is used to create the Agents in the simulation.

When creating a custom simulation, the user is encouraged not to directly use the :class:`~.agent.Agent` class, but instead use the
:class:`~.simulation.Simulation` class to create the Agents by specifying the number of Agents, the Agent type and start positions of
the agents.


.. The :class:`~.agent.Agent` class contains the following methods:

.. .. currentmodule:: src.agent

.. ====================  ============================================================================================================
.. Method                 Description
.. ====================  ============================================================================================================
.. :func:`__init__`       Creates an Agent object.
.. ====================  ============================================================================================================

.. _software_framework_communication:

Communication Module
--------------------

The :mod:`~.communication` module contains functions to handle Agent-Agent communication.
The module is used by the :class:`~.agent.Agent` class to send and receive messages to and from other Agents.

To get a simulation working, the user should never need to directly interact with the :mod:`~.communication` module. This is all handled
by the :class:`~.agent.Agent` class and the :class:`~.simulation.Simulation` class.

.. The :mod:`~.communication` module contains the following functions:

.. .. currentmodule:: src.communication

.. ====================  ============================================================================================================
.. Function              Description
.. ====================  ============================================================================================================
.. :func:`communicate`    Handles communication between Agents in a communication cluster.
.. ====================  ============================================================================================================

.. _software_framework_simulation:

Simulation Module
-----------------

The :mod:`~.simulation` module contains functionality for running and configuring a simulation.
The module is used by the :class:`~.simulation.Simulation` class to run the simulation.

Simulations can be created by initialising the :class:`~.simulation.Simulation` class and passing it the desired parameters.
These parameters are:

* The network the Agents will operate in.
* The number of Agents to create.
* The type of Agents to create.
* The start positions of the Agents.
* The filepath to save the results to.

Once the simulation is created, it can be run by calling the :func:`~.simulation.Simulation.run` method and specifying the number of
turns to run the simulation for.

A more indepth example of how to create and run a simulation can be found in the :file:`main.py` file.

.. The :mod:`~.simulation` module contains the following functions:

.. .. currentmodule:: src.simulation

.. ====================  ============================================================================================================
.. Function              Description
.. ====================  ============================================================================================================
.. :func:`run`           Runs the simulation.
.. ====================  ============================================================================================================

.. _software_framework_agent_generator:

Agent Generator Module
----------------------

The :mod:`~.agent_generator` module contains functionality for generating Agents for the simulation with the desired configuration.
The module is used by the :class:`~.simulation.Simulation` class to generate the Agents in the simulation.

To get a simulation working, the user should never need to directly interact with the :mod:`~.agent_generator` module. This is all handled
by the :class:`~.simulation.Simulation` class.

.. The :mod:`~.agent_generator` module contains the following functions:

.. .. currentmodule:: src.agent_generator
   
.. =======================  ============================================================================================================
.. Function                  Description
.. =======================  ============================================================================================================
.. :func:`generate_agents`      Generates Agents for the simulation.
.. =======================  ============================================================================================================

.. _software_framework_render:

Render Module
-------------

The :mod:`~.render` module contains functionality for graphically displaying the agents and environment in the simulation as an animation.
The module is conjunction with the :class:`~.simulation.Simulation` class to render the simulation.

For a simulation to be rendered, when not using the :file:`main.py` file, the user must pass the :class:`~.simulation.Simulation` class
to the :class:`~.render.Render` class when initialising it. Then the :func:`~.render.Render.render` method can be called to render the
simulation.

.. The :mod:`~.render` module contains the following functions:

.. .. currentmodule:: src.render

.. ====================  ============================================================================================================
.. Function              Description
.. ====================  ============================================================================================================
.. :func:`render`        Renders the simulation.
.. ====================  ============================================================================================================
