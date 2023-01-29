"""
This script tests the creation of a transmittable object
"""
# Import modules
import debug.logger as logger
# Import network
from src.network import Network
# Import belief
from src.belief import Belief
# Import transmittable
from src.transmittable import Transmittable

# Initialise logger
logger = logger.setup_logger('transmittable', './logs/transmittable.log', level='DEBUG')

# Initialise network using networks/Net1.inp
net1 = Network('networks/Net1.inp')

# Create belief - 'agent' is at node '22', the environment is net1
belief1 = Belief(net1, 'agent', '22')

# Create transmittable object
transmittable1 = Transmittable(belief1)

# Log transmittable object
logger.info(f"Transmittable object: {transmittable1}")

# Convert transmittable object to transmittable data
transmittable_data = transmittable1.to_transmittable()

# Log transmittable data
logger.info(f"Transmittable data: {transmittable_data}")

# Convert back to belief2
belief2 = Transmittable.from_transmittable(transmittable_data)

# Log belief2
logger.info(f"Belief: {belief2}")

# Check if belief2 is the same as belief1
logger.info(f"Belief 1: {belief1}")
logger.info(f"Belief 2: {belief2}")
