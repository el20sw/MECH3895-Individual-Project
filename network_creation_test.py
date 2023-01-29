"""
This script tests the creation of a network object from an EPANET input file.
"""
# Import logger
import debug.logger as logger
# Import network
from src.network import Network
# Import matplotlib.pyplot
import matplotlib.pyplot as plt

# Initialise logger
logger = logger.setup_logger('network', './logs/network.log', level='DEBUG')

# Initialise network using networks/Net1.inp
net1 = Network('networks/Net1.inp')
# Log network
logger.info(f"Network: {net1}")
# Write adjacency list to file
net1.write_adj_list_to_file('data/Net1_adj_list.json')

# Initialise network using networks/Net2.inp
net2 = Network('networks/Net2.inp')
# Log network
logger.info(f"Network: {net2}")
# Write adjacency list to file
net2.write_adj_list_to_file('data/Net2_adj_list.json')

# Initialise network using networks/Net3.inp
net3 = Network('networks/Net3.inp')
# Log network
logger.info(f"Network: {net3}")
# Write adjacency list to file
net3.write_adj_list_to_file('data/Net3_adj_list.json')

# Create figure to contain plots of networks
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
# Set figure title
fig.suptitle('Networks')
# Plot network 1
net1.plot_network(ax=axs[0])
# Plot network 2
net2.plot_network(ax=axs[1])
# Plot network 3
net3.plot_network(ax=axs[2])
# Show plots
plt.show()
