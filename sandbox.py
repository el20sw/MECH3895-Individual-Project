# Description: Sandbox for testing and debugging

# import logger
import src.debug.logger as logger
# create logger
log = logger.setup_logger(__name__, 'logs/sandbox.log', 'DEBUG')
log.getChild('src.overwatch').setLevel('DEBUG')

# import network
from src.network import Network
# import random agent
from src.random_agent import RandomAgent
# import overwatch
from src.overwatch import Overwatch

# Initialise network using networks/Net1.inp
net1 = Network('networks/Net1.inp')
log.info(f'Network: {net1}')
# Initialise random agent - agentA at node 22 in network net1 with infinite communication range
agentA = RandomAgent(net1, 'agentA', '22')
log.info(f'Agent A: {agentA}')
# Initialise another random agent - agentB at node 11 in network net1 with infinite communication range
agentB = RandomAgent(net1, 'agentB', '11')
log.info(f'Agent B: {agentB}')
# Initialise another random agent - agentC at node 33 in network net1 with infinite communication range
agentC = RandomAgent(net1, 'agentC', '31')
log.info(f'Agent C: {agentC}')
# Initialise overwatch
overwatch = Overwatch(net1, [agentA, agentB, agentC])
log.info(f'Overwatch: {overwatch}')

# make agents observe
agentA.observe(net1)
agentB.observe(net1)
agentC.observe(net1)
log.debug(f'Agent A Observation: {agentA.observation}')
log.debug(f'Agent B Observation: {agentB.observation}')
log.debug(f'Agent C Observation: {agentC.observation}')
# check agent beliefs
log.debug(f'Agent A Belief: {agentA.belief}')
log.debug(f'Agent B Belief: {agentB.belief}')
log.debug(f'Agent C Belief: {agentC.belief}')
# check agent positions
log.debug(f'Agent A Actual Position: {agentA.position}')
log.debug(f'Agent A Observed Position: {agentA.observation.position}')
log.debug(f'Agent A Belief Position: {agentA.belief.position}')
log.debug(f'Agent B Actual Position: {agentB.position}')
log.debug(f'Agent B Observed Position: {agentB.observation.position}')
log.debug(f'Agent B Belief Position: {agentB.belief.position}')
log.debug(f'Agent C Actual Position: {agentC.position}')
log.debug(f'Agent C Observed Position: {agentC.observation.position}')
log.debug(f'Agent C Belief Position: {agentC.belief.position}')

# get beliefs
beliefA = agentA.belief
beliefB = agentB.belief
beliefC = agentC.belief

# log beliefs
log.debug(f'Agent A Node Beliefs: {beliefA.nodes}')
log.debug(f'Agent B Node Beliefs: {beliefB.nodes}')
log.debug(f'Agent C Node Beliefs: {beliefC.nodes}')

# make agents communicate
# agentA.communicate(overwatch)
# agentB.communicate(overwatch)
log.debug(f'Overwatch comms buffer: {overwatch.communication_buffer}')
agentA.send_communication(overwatch)
agentB.send_communication(overwatch)
agentC.send_communication(overwatch)
log.debug(f'Overwatch comms buffer: {overwatch.communication_buffer}')
transmittablesA = agentA.receive_communication(overwatch)
transmittablesB = agentB.receive_communication(overwatch)
transmittablesC = agentC.receive_communication(overwatch)
# log the types of the transmittables
log.debug(f'Transmittables A: {[type(t) for t in transmittablesA]}')
log.debug(f'Transmittables B: {[type(t) for t in transmittablesB]}')
log.debug(f'Transmittables C: {[type(t) for t in transmittablesC]}')

log.debug(f'Overwatch comms buffer: {overwatch.communication_buffer}')
agentA.update_belief(*transmittablesA)
agentB.update_belief(*transmittablesB)

# log beliefs

log.debug(f'Agent A Node Beliefs: {beliefA.nodes}')
log.debug(f'Agent B Node Beliefs: {beliefB.nodes}')
