# Append the parent directory to the path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import tracemalloc
import src.debug.logger as logger
from src.network import Network


class TestNetwork(unittest.TestCase):
    def setUp(self):
        tracemalloc.start()
        self.logger = logger.get_logger(__name__)
        self.net1 = Network('networks/Net1.inp')
        self.logger.info(f"Network: {self.net1}")

    def test_network(self):
        self.assertIsInstance(self.net1, Network)

    def test_network_nodes(self):
        self.assertIsInstance(self.net1.node_names, list)
        self.assertEqual(len(self.net1.node_names), 11)

    def test_network_links(self):
        self.assertIsInstance(self.net1.link_names, list)
        self.assertEqual(len(self.net1.link_names), 13)


if __name__ == '__main__':
    unittest.main()
