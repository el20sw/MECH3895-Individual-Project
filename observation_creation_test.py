"""
This script tests the creation of an observation object from an environment
"""
# Import logger
import debug.logger as logger
# Import observation
from src.observation import Observation
# Import network
from src.network import Network
import matplotlib.pyplot as plt

# Initialise logger
logger = logger.setup_logger('observation', './logs/observation.log', level='DEBUG')

# Initialise network using networks/Net1.inp
net1 = Network('networks/Net1.inp')

# Create observation - 'agent' is at node '22', the environment is net1, no transmission
obs1 = Observation('11', net1)

# Check attributes of observation object can be accessed
logger.info(f"Observation: {obs1}")
logger.info(f"Position: {obs1.position}")
logger.info(f"State: {obs1.state}")

# Create observation using classmethod - 'agent' is at node '22', the environment is net1, no transmission
obs2 = Observation.observe('22', net1)

# Check attributes of observation object can be accessed
logger.info(f"Observation: {obs2}")
logger.info(f"Position: {obs2.position}")
logger.info(f"State: {obs2.state}")

# Plot the network
net1.plot_network(node_labels=True, link_labels=True)
plt.show()
