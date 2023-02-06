import src.debug.logger as logger
from src.belief import Belief
from src.network import Network
from src.transmittable import Transmittable

# create a logger
log = logger.setup_logger(file_name='logs/belief_test-1.log', level='INFO')

# create a network object
network = Network('networks/Net1.inp')

# create a belief object
beliefA = Belief(network, 'A', '10')
beliefB = Belief(network, 'B', '11')
beliefC = Belief(network, 'C', '22')
beliefD = Belief(network, 'D', '9')

log.info(f'Scenario: A, B and C are in communication range of each other, D is currently not')
log.info(f'The current positions are - A: {beliefA.position}, B: {beliefB.position}, C: {beliefC.position}, D: {beliefD.position}')
log.info(f'The agents node beliefs are - \nA: {beliefA.nodes}, \nB: {beliefB.nodes}, \nC: {beliefC.nodes}, \nD: {beliefD.nodes}')
log.info(f'The agents A, B and C share this information with each other')

# create a transmittable object
t1 = Transmittable(beliefA)
t2 = Transmittable(beliefB)
t3 = Transmittable(beliefC)
t4 = Transmittable(beliefD)

# update from transmittable
beliefA._update_from_communication(t2, t3)
beliefB._update_from_communication(t1, t3)
beliefC._update_from_communication(t1, t2)
beliefD._update_from_communication()

log.info(f'The agents believe the following positions - \nA: {beliefA.other_agents}, \nB: {beliefB.other_agents}, \nC: {beliefC.other_agents}, \nD: {beliefD.other_agents}')
log.info(f'The agents new node beliefs are - \nA: {beliefA.nodes}, \nB: {beliefB.nodes}, \nC: {beliefC.nodes}, \nD: {beliefD.nodes}')
log.info(f'Agent C moves out of communication range of A and B and into communication range of D')

beliefC._position = '32'

log.info(f'The next turn begins')

t1 = Transmittable(beliefA)
t2 = Transmittable(beliefB)
t3 = Transmittable(beliefC)
t4 = Transmittable(beliefD)

# update from transmittable
beliefA._update_from_communication(t2)
beliefB._update_from_communication(t1)
beliefC._update_from_communication(t4)
beliefD._update_from_communication(t3)

log.info(f'The agents believe the following positions - \nA: {beliefA.other_agents}, \nB: {beliefB.other_agents}, \nC: {beliefC.other_agents}, \nD: {beliefD.other_agents}')
log.info(f'The agents new node beliefs are - \nA: {beliefA.nodes}, \nB: {beliefB.nodes}, \nC: {beliefC.nodes}, \nD: {beliefD.nodes}')

log.info(f'Agent C moves such that it is in communication range of A and B as well as D')

beliefC._position = '12'

log.info(f'The next turn begins')

t1 = Transmittable(beliefA)
t2 = Transmittable(beliefB)
t3 = Transmittable(beliefC)
t4 = Transmittable(beliefD)

# update from transmittable
beliefA._update_from_communication(t2, t3)
beliefB._update_from_communication(t1, t3)
beliefC._update_from_communication(t1, t2, t4)
beliefD._update_from_communication(t3)

log.info(f'The agents believe the following positions - \nA: {beliefA.other_agents}, \nB: {beliefB.other_agents}, \nC: {beliefC.other_agents}, \nD: {beliefD.other_agents}')
log.info(f'The agents new node beliefs are - \nA: {beliefA.nodes}, \nB: {beliefB.nodes}, \nC: {beliefC.nodes}, \nD: {beliefD.nodes}')
