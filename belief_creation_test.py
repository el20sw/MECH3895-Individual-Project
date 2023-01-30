"""
This script tests the creation of a belief state object from an environment
"""
# Import logger
import src.debug.logger as logger
# Import belief
from src.belief import Belief
# Import network
from src.network import Network
# Import observation
from src.observation import Observation
# Import transmittable
from src.transmittable import Transmittable

# Initialise logger
logger = logger.setup_logger('belief', './logs/belief.log', level='DEBUG')

# Initialise network using networks/Net1.inp
net1 = Network('networks/Net1.inp')
logger.info(f"Network: {net1}")

# Initialise belief state
belief1 = Belief(net1, 'A', '22')
belief2 = Belief(net1, 'B', '12')
logger.info(f"Belief state A: {belief1}")
logger.info(f"Belief state B: {belief2}")

# Create an observation object
observationA = Observation(environment=net1, position='22')
ObservationB = Observation(environment=net1, position='12')
logger.info(f"Observation A: {observationA}")
logger.info(f"Observation B: {ObservationB}")

# Create a transmittable objects
transmittableA_B = Transmittable(belief1)
transmittableB_A = Transmittable(belief2)
logger.info(f"Transmittable A to B: {transmittableA_B}")
logger.info(f"Transmittable B to A: {transmittableB_A}")

# Check attributes of belief state object can be accessed
logger.info(f"Agent ID: {belief1.agent_id}")
logger.info(f"Position: {belief1.position}")
logger.info(f"Nodes: {belief1.nodes}")
logger.info(f"Links: {belief1.links}")

# Check nodes in belief state are the same as nodes in network
logger.info(f"Nodes in belief state: {list(belief1.nodes.keys())}")
logger.info(f"Nodes in network: {net1.node_names}")

# Log the belief state of A and B
logger.info(f"Belief state of A: {belief1.nodes}")
logger.info(f"Belief state of B: {belief2.nodes}")

# Update the belief state of A
belief1.update(observationA, transmittableB_A)

# Log the belief state of A and B
logger.info(f"Belief state of A: {belief1.nodes}")
logger.info(f"Belief state of B: {belief2.nodes}")
