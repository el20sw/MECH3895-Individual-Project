# Append the parent directory to the path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from src.network import Network
from src.belief import Belief
from src.observation import Observation
from src.transmittable import Transmittable


class TestBelief(unittest.TestCase):
    def setUp(self):
        self.network = Network('networks/Net1.inp')
        self.belief = Belief(self.network, 'A', '11')

    def test_belief(self):
        """
        Test that the belief is an instance of the Belief class
        """
        self.assertIsInstance(self.belief, Belief)

    def test_property_agent(self):
        """
        Test that the agent_id property is set correctly
        """
        self.assertEqual(self.belief.agent_id, 'A')

    def test_property_position(self):
        """
        Test that the position property is set correctly
        """
        self.assertEqual(self.belief.position, '11')
        
    def test_property_nodes(self):
        """
        Test that the nodes property is set correctly
        """
        self.assertIsInstance(self.belief.nodes, dict)
        self.assertDictEqual(self.belief.nodes, {'10': 1, '11': 0, '12': 1, '13': 1, '21': 1, '22': 1, '23': 1, '31': 1, '32': 1, '2': 1, '9': 1})

    def test_property_unvisited_nodes(self):
        """
        Test that the unvisited_nodes property is set correctly
        """
        self.assertIsInstance(self.belief.unvisited_nodes, list)
        self.assertListEqual(self.belief.unvisited_nodes, ['10', '12', '13', '21', '22', '23', '31', '32', '2', '9'])

    def test_property_visited_nodes(self):
        """
        Test that the visited_nodes property is set correctly
        """
        self.assertIsInstance(self.belief.visited_nodes, list)
        self.assertListEqual(self.belief.visited_nodes, ['11'])

    def test_property_occupied_nodes(self):
        """
        Test that the occupied_nodes property is set correctly
        """
        self.assertIsInstance(self.belief.occupied_nodes, list)
        self.assertListEqual(self.belief.occupied_nodes, [])

    def test_property_links(self):
        """
        Test that the links property is set correctly
        """
        self.assertIsInstance(self.belief.links, list)
        self.assertListEqual(self.belief.links, [])

    def test_method_update(self):
        """
        Test that the update method updates the belief correctly
        """
        self.observation = Observation(self.network, '12')
        self.belief.update(self.observation)
        self.assertEqual(self.belief.position, '12')
        self.assertDictEqual(self.belief.nodes, {'10': 1, '11': 0, '12': 0, '13': 1, '21': 1, '22': 1, '23': 1, '31': 1, '32': 1, '2': 1, '9': 1})
        self.assertListEqual(self.belief.unvisited_nodes, ['10', '13', '21', '22', '23', '31', '32', '2', '9'])
        self.assertListEqual(self.belief.visited_nodes, ['11', '12'])
        self.assertListEqual(self.belief.occupied_nodes, [])
        self.assertListEqual(self.belief.links, [('12', '11', {'link_name' : self.network.adj_list['12']['11']['link_name'], 'link_length' : self.network.adj_list['12']['11']['link_length']})])

        """
        Test that the update_from_observation method updates the belief correctly
        """
        self.observation = Observation(self.network, '22')
        self.belief.update(self.observation)
        self.assertEqual(self.belief.position, '22')
        self.assertDictEqual(self.belief.nodes, {'10': 1, '11': 0, '12': 0, '13': 1, '21': 1, '22': 0, '23': 1, '31': 1, '32': 1, '2': 1, '9': 1})
        self.assertListEqual(self.belief.unvisited_nodes, ['10', '13', '21', '23', '31', '32', '2', '9'])
        self.assertListEqual(self.belief.visited_nodes, ['11', '12', '22'])
        self.assertListEqual(self.belief.occupied_nodes, [])
        self.assertListEqual(self.belief.links, [
            ('12', '11', {'link_name' : self.network.adj_list['12']['11']['link_name'], 'link_length' : self.network.adj_list['12']['11']['link_length']}), 
            ('22', '12', {'link_name' : self.network.adj_list['22']['12']['link_name'], 'link_length' : self.network.adj_list['22']['12']['link_length']})])

        """
        Test that the update_from_communication method updates the belief correctly
        """

        # New 'agent' at position '32'
        beliefA = Belief(self.network, 'B', '32')
        self.assertEqual(beliefA.position, '32')

        # New 'agent' moves to position '31
        observationA = Observation(self.network, '31')
        beliefA.update(observationA)
        self.assertEqual(beliefA.position, '31')

        transmittable = Transmittable(beliefA)

        self.belief.update(transmittable)
        self.assertEqual(self.belief.position, '22')
        self.assertDictEqual(self.belief.nodes, {'10': 1, '11': 0, '12': 0, '13': 1, '21': 1, '22': 0, '23': 1, '31': -10, '32': 0, '2': 1, '9': 1})
        self.assertListEqual(self.belief.unvisited_nodes, ['10', '13', '21', '23', '2', '9'])
        self.assertListEqual(self.belief.visited_nodes, ['11', '12', '22', '32'])
        self.assertListEqual(self.belief.occupied_nodes, ['31'])
        self.assertListEqual(self.belief.links, [
            ('12', '11', {'link_name' : self.network.adj_list['12']['11']['link_name'], 'link_length' : self.network.adj_list['12']['11']['link_length']}), 
            ('22', '12', {'link_name' : self.network.adj_list['22']['12']['link_name'], 'link_length' : self.network.adj_list['22']['12']['link_length']}), 
            ('31', '32', {'link_name' : self.network.adj_list['31']['32']['link_name'], 'link_length' : self.network.adj_list['31']['32']['link_length']}),
            ])

        # 'Agent' moves to position '23
        self.observation = Observation(self.network, '23')
        self.belief.update(self.observation)        

        # New 'agent' at position '21'
        observationB = Observation(self.network, '21')
        beliefA.update(observationB)
        self.assertEqual(beliefA.position, '21')

        transmittable = Transmittable(beliefA)

        self.belief.update(transmittable)
        self.assertEqual(self.belief.position, '23')
        self.assertDictEqual(self.belief.nodes, {'10': 1, '11': 0, '12': 0, '13': 1, '21': -10, '22': 0, '23': 0, '31': 0, '32': 0, '2': 1, '9': 1})
        self.assertListEqual(self.belief.unvisited_nodes, ['10', '13', '2', '9'])
        self.assertListEqual(self.belief.visited_nodes, ['11', '12', '22', '23', '31', '32'])
        self.assertListEqual(self.belief.occupied_nodes, ['21'])
        self.assertListEqual(self.belief.links, [
            ('12', '11', {'link_name' : self.network.adj_list['12']['11']['link_name'], 'link_length' : self.network.adj_list['12']['11']['link_length']}),
            ('22', '12', {'link_name' : self.network.adj_list['22']['12']['link_name'], 'link_length' : self.network.adj_list['22']['12']['link_length']}),
            ('31', '32', {'link_name' : self.network.adj_list['31']['32']['link_name'], 'link_length' : self.network.adj_list['31']['32']['link_length']}),
            ('23', '22', {'link_name' : self.network.adj_list['23']['22']['link_name'], 'link_length' : self.network.adj_list['23']['22']['link_length']}),
            ('21', '31', {'link_name' : self.network.adj_list['21']['31']['link_name'], 'link_length' : self.network.adj_list['21']['31']['link_length']}),            
            ])
        

if __name__ == '__main__':
    unittest.main()

