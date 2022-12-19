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

    # Method to add a node to the network
    def add_node(self, node_id):
        # Create a node object
        node = Node(node_id)
        # Add the node to the set of nodes
        self.nodes.add(node)
        # Create an empty adjacency list for the node
        self.adjacency_list[node.get_id()] = set()

    # Method to add a pipe to the network
    def add_pipe(self, pipe_length, node1_id, node2_id):
        # Create a pipe object
        pipe = Pipe(pipe_length)
        # Add the pipe to the adjacency list for both nodes with information about the connected node
        self.adjacency_list[node1_id].add((node2_id, pipe))
        self.adjacency_list[node2_id].add((node1_id, pipe))

    # Method to get the nodes in the network
    def get_nodes(self):
        return self.nodes

    # Method to get the adjacency list for the network
    def get_adjacency_list(self):
        return self.adjacency_list

    # Method to print the network
    def print_network(self):
        # Print the nodes        
        for node in self.adjacency_list.keys():
            print(f"Node {node} : {self.adjacency_list[node]}")

    # Method to draw the network
    def draw_network(self):
        # Create an undirected graph
        graph = nx.Graph()
        # Add the nodes to the graph
        for node in self.nodes:
            graph.add_node(node.get_id())
        # Add the edges to the graph
        for node in self.adjacency_list:
            for connected_node in self.adjacency_list[node]:
                graph.add_edge(node, connected_node[0])
        # Add edge labels to the graph
        edge_labels = {}
        for node in self.adjacency_list:
            for connected_node in self.adjacency_list[node]:
                edge_labels[(node, connected_node[0])] = connected_node[1].get_length()
        nx.set_edge_attributes(graph, edge_labels, 'length')
        # Draw the graph
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        # Show the graph
        plt.show()
