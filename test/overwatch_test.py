# Append the parent directory to the path
from context import src

import unittest
import tracemalloc
import src.debug.logger as logger
from src.network import Network
from src.agents.random_agent import RandomAgent
from src.overwatch import Overwatch

class TestOverwatch(unittest.TestCase):
    """
    Test Case for Overwatch
    """
    def setUp(self):
        tracemalloc.start()
        self.logger = logger.get_logger(__name__)
        self.net1 = Network('networks/Net1.inp')
        self.agent1 = RandomAgent(self.net1, 'A', '11')
        self.agent2 = RandomAgent(self.net1, 'B', '10')
        self.agent3 = RandomAgent(self.net1, 'C', '9')
        self.overwatch = Overwatch(self.net1, [self.agent1, self.agent2, self.agent3])

    def test_overwatch(self):
        self.assertIsInstance(self.overwatch, Overwatch)

if __name__ == '__main__':
    unittest.main()