"""
This script tests the creation of a belief state object from an environment
"""
# Import logger
import debug.logger as logger
# Import belief
from src.belief import Belief
# Import network
from src.network import Network

# Initialise logger
logger = logger.setup_logger('belief', './logs/belief.log', level='DEBUG')

# Initialise network using networks/Net1.inp
net1 = Network('networks/Net1.inp')
# Log network
logger.info(f"Network: {net1}")

# Initialise belief state
belief1 = Belief(net1)

# Check attributes of belief state object can be accessed
logger.info(f"Belief state: {belief1}")
logger.info(f"Agent ID: {belief1.agent_id}")
logger.info(f"Position: {belief1.position}")
logger.info(f"Nodes: {belief1.nodes}")
logger.info(f"Links: {belief1.links}")

# Check nodes in belief state are the same as nodes in network
logger.info(f"Nodes in belief state: {list(belief1.nodes.keys())}")
logger.info(f"Nodes in network: {net1.node_names}")

# Update belief state
belief1.update(net1, 'move', 'J1')
