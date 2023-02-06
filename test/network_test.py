from context import src

import unittest
import wntr

from src.network import Network
from src.keys import FrozenLinks, FrozenNodes

class TestNetwork(unittest.TestCase):
    """
    Testing Network Class
    """
    def setUp(self):
        self.network = Network('networks/Net1.inp')
        self._wn = wntr.network.WaterNetworkModel('networks/Net1.inp')
        self._wn_dict = wntr.network.to_dict(self._wn)

    def test_property_links(self):
        self.assertIsInstance(self.network.links, list)
        self.assertEqual(self.network.links, self._wn_dict['links'])

    def test_property_link_names(self):
        self.assertIsInstance(self.network.link_names, list)
        self.assertEqual(self.network.link_names, self._wn.link_name_list)

    def test_property_pipes(self):
        self.assertIsInstance(self.network.pipes, list)
        self.assertEqual(self.network.pipes, [link for link in self._wn_dict['links'] if link['link_type'] == 'Pipe'])

    def test_property_pipe_names(self):
        self.assertIsInstance(self.network.pipe_names, list)
        self.assertEqual(self.network.pipe_names, self._wn.pipe_name_list)

    def test_property_nodes(self):
        self.assertIsInstance(self.network.nodes, list)
        self.assertEqual(self.network.nodes, self._wn_dict['nodes'])

    def test_property_node_names(self):
        self.assertIsInstance(self.network.node_names, list)
        self.assertEqual(self.network.node_names, self._wn.node_name_list)

    def test_property_junctions(self):
        self.assertIsInstance(self.network.junctions, list)
        self.assertEqual(self.network.junctions, [node for node in self._wn_dict['nodes'] if node['node_type'] == 'Junction'])

    def test_property_junction_names(self):
        self.assertIsInstance(self.network.junction_names, list)
        self.assertEqual(self.network.junction_names, self._wn.junction_name_list)

    def test_property_adj_list(self):
        adj_list = self.network.adj_list
        self.assertIsInstance(adj_list, dict)
        for start_node, end_nodes in adj_list.items():
            self.assertIn(start_node, self.network.node_names)
            self.assertIsInstance(end_nodes, dict)
            for end_node, link_dict in end_nodes.items():
                self.assertIn(end_node, self.network.node_names)
                self.assertIsInstance(link_dict, dict)
                self.assertIn('link_name', link_dict)
                self.assertIn(link_dict['link_name'], self.network.link_names)
                self.assertIn('link_length', link_dict)
                self.assertIsInstance(link_dict['link_length'], (int, float))

if __name__ == '__main__':
    unittest.main()
