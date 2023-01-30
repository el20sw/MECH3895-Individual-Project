### Import modules
import src.debug.logger as logger

import wntr
import matplotlib.pyplot as plt

import os
import json
import math

from src.keys import FrozenNodes, FrozenLinks

### Pipe Network Class ###
class Network:
    """
    Pipe Network Class
    ----------
    :param path_to_file: Path to the input file - .inp file
    """

    def __init__(self, path_to_file) -> None:
        # Initialise logger
        self.logger = logger.get_logger(__name__)

        # Initialise network
        self._wn = wntr.network.WaterNetworkModel(path_to_file)

        # Initialise network dictionary
        self._wn_dict = wntr.network.to_dict(self._wn)
        
        # Properties
        self._links = self._wn_dict['links']
        self._link_names = self._wn.link_name_list
        self._pipes = [link for link in self._links if link['link_type'] == 'Pipe']
        self._pipe_names = self._wn.pipe_name_list
        self._link_lengths = self._wn.query_link_attribute('length')

        self._nodes = self._wn_dict['nodes']
        self._node_names = self._wn.node_name_list
        self._junctions = [node for node in self._nodes if node['node_type'] == 'Junction']
        self._junction_names = self._wn.junction_name_list

        # Create frozen nodes and links
        self._frozen_nodes = FrozenNodes(self._node_names)
        self._frozen_links = FrozenLinks(self._link_names)

        # Initialise adjacency list
        self._adj_list = {}
        # Build adjacency list
        self._adj_list = self._get_adj_list()

    @property
    def links(self) -> list:
        return self._links

    @property
    def link_names(self) -> list:
        return self._link_names

    @property
    def pipes(self) -> list:
        return self._pipes

    @property
    def pipe_names(self) -> list:
        return self._pipe_names

    @property
    def nodes(self) -> list:
        return self._nodes

    @property
    def node_names(self) -> list:
        return self._node_names

    @property
    def junctions(self) -> list:
        return self._junctions

    @property
    def junction_names(self) -> list:
        return self._junction_names

    @property
    def frozen_nodes(self) -> FrozenNodes:
        return self._frozen_nodes

    @property
    def frozen_links(self) -> FrozenLinks:
        return self._frozen_links

    @property
    def adj_list(self) -> dict:
        return self._adj_list
    
    # Get adjacency list
    def _get_adj_list(self) -> dict:
        """
        Method to get adjacency list - if there is a node and a link, the robots can traverse them
        If no link length is specified, i.e. in the case of a pump, the link length is calculated using the coordinates of the start and end nodes
        :return: Adjacency list
        """
        # Iterate through links and add start_node and end_node to adjacency list
        for link in self._links:
            # Get start and end nodes
            start_node = link['start_node_name']
            end_node = link['end_node_name']
            # Get link name
            link_name = link['name']
            # Add start and end nodes to adjacency list
            if start_node not in self._adj_list:
                self._adj_list[start_node] = {}
            if end_node not in self._adj_list:
                self._adj_list[end_node] = {}
            # Add link to adjacency list
            self._adj_list[start_node][end_node] = {
                'link_name': link_name,
                'link_length': link['length'] if 'length' in link else self.calculate_link_length(start_node, end_node)
                }
            self._adj_list[end_node][start_node] = {
                'link_name': link_name,
                'link_length': link['length'] if 'length' in link else self.calculate_link_length(start_node, end_node)
                }
        return self._adj_list

    # Method to calculate the length of a link using the coordinates of the start and end nodes
    def calculate_link_length(self, start_node, end_node) -> float:
        """
        Method to calculate the length of a link using the coordinates of the start and end nodes
        :param start_node: Start node
        :param end_node: End node
        :return: Length of the link
        """
        # Get coordinates of start and end nodes
        start_node = self._wn.get_node(start_node)
        end_node = self._wn.get_node(end_node)
        # try to get the coordinates
        start_node_coords = getattr(start_node, 'coordinates', None)
        end_node_coords = getattr(end_node, 'coordinates', None)
        # If the coordinates are not None, calculate the length of the link
        if start_node_coords is not None and end_node_coords is not None:
            return math.sqrt((start_node_coords[0] - end_node_coords[0])**2 + (start_node_coords[1] - end_node_coords[1])**2)
        # If the coordinates are None, return 10
        else:
            return 10

    # Method to write the adjacency list to a file
    def write_adj_list_to_file(self, path_to_file) -> None:
        """
        Method to write the adjacency list to a json file
        :param path_to_file: Path to the file
        :return: None
        """
        # Get adjacency list
        self._get_adj_list()

        # Check if the directory exists
        if not os.path.exists(os.path.dirname(path_to_file)):
            # If it doesn't, create it
            os.makedirs(os.path.dirname(path_to_file))
        
        # Try to write the adjacency list to a file
        try:
            with open(path_to_file, 'w') as f:
                json.dump(self._adj_list, f, indent=4)
        # If there is an error, log it
        except Exception as e:
            self.logger.error(f"Error writing adjacency list to file: {e}")

    # Method for an agent to request the state of the network
    def get_state(self, node) -> dict:
        """
        Method for an agent to request the state of the network at a node level
        - Currently this gives the keys (node names) of the nodes that are connected to the node
        :return: State of the network at a node - currently this is the keys (node names) of the nodes that are connected to the node
        """
        if node not in self._frozen_nodes.frozen_node_keys:
            raise ValueError(f"Node {node} is not valid")
        state = {
            'node': node,
            'neighbours': list(self._adj_list[node].keys()),
        }

        return state

    # Method to get links from a node
    def get_links(self, node) -> list:
        """
        Method to get links from a node
        :param node: Node
        :return: List of links
        """
        # Get adjacency list
        self._get_adj_list()

        # Get links
        links = []
        for dest_node in self._adj_list[node]:
            links.append((node, dest_node, self._adj_list[node][dest_node]['link_length']))
        return links

    # Method to plot the network using wntr graphics api
    def plot_network(self, *args, **kwargs) -> None:
        """
        Method to plot the network
        :param args: Arguments to pass to the wntr.graphics.plot_network method
        :param kwargs: Keyword arguments to pass to the wntr.graphics.plot_network method
        :return: None
        """
        # Plot the network
        wntr.graphics.plot_network(self._wn, *args, **kwargs)