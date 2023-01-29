"""
This script tests the creation of a network object from an EPANET input file.
"""
# Import logger
import debug.logger as logger
# Import network
from src.network import Network

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