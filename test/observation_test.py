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
        self.log = logger.get_logger(__name__)
        tracemalloc.start()
        self.net1 = Network('networks/Net1.inp')
        self.obs1 = Observation(self.net1, '11')

    def test_observation(self):
        self.assertIsInstance(self.obs1, Observation)

    def test_observation_position(self):
        self.assertIsInstance(self.obs1.position, str)
        self.assertEqual(self.obs1.position, '11')

    def test_observation_state(self):
        self.assertIsInstance(self.obs1.state, dict)
        self.assertDictEqual(self.obs1.state, {'node' : '11', 'neighbours' : ['10', '12', '21']})


if __name__ == '__main__':
    unittest.main()
