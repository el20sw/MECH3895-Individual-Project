from context import src

import unittest
import tracemalloc

import src.debug.logger as logger

from src.simulation import Simulation
from src.network import Network
from src.random_agent import RandomAgent

class TestSimulation(unittest.TestCase):
    """
    Testing Simulation Class
    """
    def setUp(self):
        tracemalloc.start()
        self.logger = logger.get_logger(__name__)
        self.net1 = Network('networks/Net1.inp')
        self.agent1 = RandomAgent(self.net1, 'A', '11')
        self.sim1 = Simulation(self.net1)

    def test_simulation(self):
        self.assertIsInstance(self.sim1, Simulation)

    def test_simulation_environment(self):
        self.assertIsInstance(self.sim1._environment, Network)
        self.assertEqual(self.sim1._environment, self.net1)

    def test_simulation_turns(self):
        self.assertIsInstance(self.sim1._turns, int)
        self.assertEqual(self.sim1._turns, 0)

    def test_simulation_agents(self):
        self.assertIsInstance(self.sim1._agents, list)
        self.assertEqual(self.sim1._agents, [])

    def test_simulation_add_agent(self):
        self.sim1.add_agent(self.agent1)
        self.assertIsInstance(self.sim1._agents, list)
        self.assertEqual(self.sim1._agents, [self.agent1])

    def test_simulation_remove_agent(self):
        self.sim1.add_agent(self.agent1)
        self.sim1.remove_agent(self.agent1)
        self.assertIsInstance(self.sim1._agents, list)
        self.assertEqual(self.sim1._agents, [])

    def test_simulation_run(self):
        self.sim1.add_agent(self.agent1)
        self.sim1.run(10)
        self.assertIsInstance(self.sim1._turns, int)
        self.assertEqual(self.sim1._turns, 10)

    def test_simulation_results(self):
        self.sim1.add_agent(self.agent1)
        self.sim1.run(10)
        self.assertIsInstance(self.sim1.results, dict)

    def test_simulation_write_results(self):
        self.sim1.add_agent(self.agent1)
        self.sim1.run(10)
        self.sim1.write_results('test/results/test_results.json')
        self.assertIsInstance(self.sim1.results, dict)

if __name__ == '__main__':
    unittest.main()
