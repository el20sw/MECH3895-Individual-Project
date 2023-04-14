Installation
=============

Pre-amble
---------

This project was developed using Python 3.8.10 in an Ubuntu Linux OS and hasn't been tested on any other version. 
It is recommended to use a virtual environment to install the dependencies.

Installation
------------

To create a virtual environment, run the following command or use your preferred method:

    :code:`python3 -m venv venv`

To activate the virtual environment, run the following command or use your preferred method:
    
    :code:`source venv/bin/activate`

To install the dependencies, run the following command:

    :code:`pip install -r requirements.txt`

To create and run a simulation, run the following command:

    :code:`python3 main.py`

This will use a Command Line Interface (CLI) to ask for the parameters of the simulation. When prompted to
enter start positions, network maps can be found in the `networks` folder though the larger network images do not have node labels due to the
size of the maps. In that case, it is recommended to use the `.json` or `.inp` source files in the `networks` folder to retrieve the
desired node labels - apologies for the inconvenience.
