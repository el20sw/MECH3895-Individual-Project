# Append the parent directory to the path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import tracemalloc
import src.debug.logger as logger
from src.network import Network
from src.observation import Observation

class TestObservation(unittest.TestCase):
    """
    Testing Observation Class
    """
    def setUp(self):
        self.network = Network('networks/Net1.inp')
        self.observation = Observation(self.network, '11')

    def test_observation(self):
        self.assertIsInstance(self.observation, Observation)

    def test_position(self):
        self.assertIsInstance(self.observation.position, str)
        self.assertEqual(self.observation.position, '11')

    def test_state(self):
        self.assertIsInstance(self.observation.state, dict)
        self.assertDictEqual(self.observation.state, {'node' : '11', 'neighbours' : ['10', '12', '21']})

    def test_observe(self):
        self.observe = Observation.observe(self.network, '11')
        self.assertIsInstance(self.observe, Observation)
        self.assertEqual(self.observe.position, '11')
        self.assertDictEqual(self.observe.state, {'node' : '11', 'neighbours' : ['10', '12', '21']})

if __name__ == '__main__':
    unittest.main()
