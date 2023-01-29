"""
This script tests the creation of an observation object from an environment
"""
# Import logger
import debug.logger as logger
# Import observation
from src.observation import Observation
# Import network
from src.network import Network
# Import agent
from src.agent import Agent

# Initialise logger
logger = logger.setup_logger('observation', './logs/observation.log', level='DEBUG')

# Initialise network using networks/Net1.inp
net1 = Network('networks/Net1.inp')

# Create observation - 'agent' is at node '22', the environment is net1, no transmission
obs1 = Observation('agent', '22', net1)

