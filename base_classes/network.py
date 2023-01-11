# Imports
from base_classes.node import Node
from base_classes.pipe import Pipe

import networkx as nx
import matplotlib.pyplot as plt

# Class representing a network in the system (a network is a collection of nodes and pipes)
class Network:
    # Constructor for the network class
    def __init__(self):
        # Create an empty set of nodes
        self.nodes = set()
        # Create an empty adjacency list
        self.adjacency_list = {}

    # Method to add connections to the network
    def add_connection(self, node1_id, node2_id, pipe_length, angle=None):
        # Add the nodes to the network
        if node1_id not in self.adjacency_list:
            # Create a node object
            node = Node(node1_id)
            # Add the node to the set of nodes
            self.nodes.add(node)
            self.adjacency_list[node.get_id()] = {}
        if node2_id not in self.adjacency_list:
            # Create a node object
            node = Node(node2_id)
            # Add the node to the set of nodes
            self.nodes.add(node)
            self.adjacency_list[node.get_id()] = {}

        # Create a pipe object
        pipe = Pipe(pipe_length)
        # Add the pipe and angle to the adjacency list for both nodes
        if angle is not None:
            self.adjacency_list[node1_id][node2_id] = (pipe, angle)
            self.adjacency_list[node2_id][node1_id] = (pipe, 180 + angle)

        else:
            self.adjacency_list[node1_id][node2_id] = (pipe,)
            self.adjacency_list[node2_id][node1_id] = (pipe,)

    # Method to get the nodes in the network
    def get_node(self):
        return self.nodes

    # Method to get the node ids in the network
    def get_node_ids(self):
        return {node.get_id() for node in self.nodes}

    # Method to get the adjacency list of the network
    def get_adjacency_list(self):
        return self.adjacency_list

    # Method to get local adjacency list given a node
    def get_local_adjacency_list(self, node_id):
        return self.adjacency_list[node_id]

    # Method to get the possible moves given a current location
    def get_possible_moves(self, current_location):
        possible_moves = list(self.get_local_adjacency_list(current_location).keys())
        return possible_moves

    # Method to get the length of a pipe from the adjacency list given a start and end node
    def get_pipe_length(self, node1_id, node2_id):
        if node2_id in self.adjacency_list[node1_id]:
            return self.adjacency_list[node1_id][node2_id][0].get_length()
    

    # Method to print the network
    def print_network(self):
        # Print the adjacency list
        for node in self.adjacency_list:
            print(f'Node {node} : {self.adjacency_list[node]}')

    # Method to pretty print the network
    def pretty_print_network(self):
        # Print the adjacency list
        for node1_id in self.adjacency_list:
            for node2_id in self.adjacency_list[node1_id]:
                print('{} -> {} : {}'.format(node1_id, node2_id, self.adjacency_list[node1_id][node2_id]))

    # Method to draw the network
    def draw_network(self):
        # Create a graph object
        graph = nx.Graph()
        # Add nodes to the graph
        for node in self.nodes:
            graph.add_node(node.get_id())
        # Add edges to the graph
        for node1_id in self.adjacency_list:
            for node2_id in self.adjacency_list[node1_id]:
                graph.add_edge(node1_id, node2_id)
        # Add labels to the edges
        edge_labels = {}
        for node in self.adjacency_list:
            for neighbour in self.adjacency_list[node]:
                edge_labels[(node, neighbour)] = self.adjacency_list[node][neighbour][0].get_length()
        nx.set_edge_attributes(graph, edge_labels, 'length')
        # Draw the graph
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        # Show the graph
        plt.show()
