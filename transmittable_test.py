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
# Create belief - 'agent' is at node '11', the environment is net1
belief2 = Belief(net1, 'agent', '11')

# Create transmittable object
transmittable1 = Transmittable(belief1, belief2)

# Log transmittable object
logger.info(f"Transmittable object: {transmittable1}")

# Unpack transmittable object
_ = transmittable1.objects

# Log unpacked transmittable object
logger.info(f"Unpacked transmittable object: {_}")

# Get the first belief
a = transmittable1.objects[0]
# Get the second belief
b = transmittable1.objects[1]

# Log the first belief
logger.info(f"First belief: {a}")
logger.info(f"First position: {a.position}")
logger.info(f"First nodes: {a.nodes}")
# Log the second belief
logger.info(f"Second belief: {b}")
logger.info(f"Second nodes: {b.nodes}")
