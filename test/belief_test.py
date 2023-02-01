# Append the parent directory to the path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import tracemalloc

import src.debug.logger as logger
from src.network import Network
from src.overwatch import Overwatch
from src.random_agent import RandomAgent
from src.transmittable import Transmittable

class TestBelief(unittest.TestSuite):
    def __init__(self):
        super().__init__()
        self.addTest(TestUpdateBelief('test_update_belief'))

class TestUpdateBelief(unittest.TestCase):
    def setUp(self):
        tracemalloc.start()
        self.logger = logger.setup_logger(__name__, 'logs/test_update_belief.log', 'DEBUG')
        self.net1 = Network('networks/Net1.inp')
        self.agent1 = RandomAgent(self.net1, 'A', '11')
        self.agent2 = RandomAgent(self.net1, 'B', '22')
        self.agent3 = RandomAgent(self.net1, 'C', '32')
        self.overwatch = Overwatch(self.net1, [self.agent1, self.agent2, self.agent3])

    def test_update_belief_part1(self):
        self.logger.debug('Testing update_belief()')
        self.logger.debug('Initialising agents')
        self.agent1.observe(self.net1)
        self.agent2.observe(self.net1)
        self.agent3.observe(self.net1)
        belief1 = self.agent1.belief
        belief2 = self.agent2.belief
        belief3 = self.agent3.belief
        self.logger.debug('Initialising transmittables')
        transmittable_b1 = Transmittable(belief1)
        transmittable_b2 = Transmittable(belief2)
        transmittable_b3 = Transmittable(belief3)
        self.logger.debug('Updating beliefs')
        self.agent1.update_belief(transmittable_b2, transmittable_b3)
        self.agent2.update_belief(transmittable_b1, transmittable_b3)
        self.agent3.update_belief(transmittable_b1, transmittable_b2)
        self.logger.debug('Checking beliefs')
        agent1_end_belief = {'10': 1, '11': 0, '12': 1, '13': 1, '21': 1, '22': -10, '23': 1, '31': 1, '32': -10, '2': 1, '9': 1}
        agent2_end_belief = {'10': 1, '11': -10, '12': 1, '13': 1, '21': 1, '22': 0, '23': 1, '31': 1, '32': -10, '2': 1, '9': 1}
        agent3_end_belief = {'10': 1, '11': -10, '12': 1, '13': 1, '21': 1, '22': -10, '23': 1, '31': 1, '32': 0, '2': 1, '9': 1}
        self.assertDictEqual(self.agent1.belief.nodes, agent1_end_belief)
        self.assertDictEqual(self.agent2.belief.nodes, agent2_end_belief)
        self.assertDictEqual(self.agent3.belief.nodes, agent3_end_belief)

    def test_update_belief_part2(self):
        self.logger.debug('Testing update_belief()')
        self.logger.debug('Moving agents')
        self.agent1._position = '12'
        self.agent2._position = '21'
        self.agent3._position = '31'
        self.logger.debug('Initialising agents')
        self.agent1.observe(self.net1)
        self.agent2.observe(self.net1)
        self.agent3.observe(self.net1)
        belief1 = self.agent1.belief
        belief2 = self.agent2.belief
        belief3 = self.agent3.belief
        self.logger.debug('Initialising transmittables')
        transmittable_b1 = Transmittable(belief1)
        transmittable_b2 = Transmittable(belief2)
        transmittable_b3 = Transmittable(belief3) 
        self.logger.debug('Updating beliefs')
        self.agent1.update_belief(transmittable_b2, transmittable_b3)
        self.agent2.update_belief(transmittable_b1, transmittable_b3)
        self.agent3.update_belief(transmittable_b1, transmittable_b2)
        self.logger.debug('Checking beliefs')
        agent1_end_belief = {'10': 1, '11': 0, '12': 0, '13': 1, '21': -10, '22': 0, '23': 1, '31': -10, '32': 0, '2': 1, '9': 1}
        agent2_end_belief = {'10': 1, '11': 0, '12': -10, '13': 1, '21': 0, '22': 0, '23': 1, '31': -10, '32': 0, '2': 1, '9': 1}
        agent3_end_belief = {'10': 1, '11': 0, '12': -10, '13': 1, '21': -10, '22': 0, '23': 1, '31': 0, '32': 0, '2': 1, '9': 1}
        self.assertDictEqual(self.agent1.belief.nodes, agent1_end_belief)
        self.assertDictEqual(self.agent2.belief.nodes, agent2_end_belief)
        self.assertDictEqual(self.agent3.belief.nodes, agent3_end_belief)

    def tearDown(self):
        self.logger.debug('Testing complete')
        self.logger.debug('Testing memory usage')
        current, peak = tracemalloc.get_traced_memory()
        self.logger.debug(f'Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB')
        tracemalloc.stop()

if __name__ == '__main__':
    unittest.main()

