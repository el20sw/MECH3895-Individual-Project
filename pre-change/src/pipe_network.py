### Import modules
import copy
import wntr
import matplotlib.pyplot as plt

### Pipe Network Class ###
class PipeNetwork:
    ### Constructor
    def __init__(self, path_to_file):
        self.wn = wntr.network.WaterNetworkModel(path_to_file)
        self.wn_dict = wntr.network.to_dict(self.wn)
        self.graph = wntr.network.to_graph(self.wn)
        self.undirected_graph = self.graph.to_undirected()

        self.wn_links = self.wn_dict['links']
        self.link_lengths = self.wn.query_link_attribute('length')
        self.link_names = self.wn.link_name_list
        self.wn_pipes = [link for link in self.wn_links if link['link_type'] == 'Pipe']
        
        self.wn_nodes = self.wn_dict['nodes']
        self.node_names = self.wn.node_name_list
        self.wn_junctions = [node for node in self.wn_nodes if node['node_type'] == 'Junction']
        self.junction_names = self.wn.junction_name_list
        
        self.adj_list = {}

    # Get adjacency list
    def get_adj_list(self):
        """
        Method to get adjacency list - filters out non-pipe links
        :return: Adjacency list
        """
        # Iterate through pipes and add start_node to adjacency list and end_node to adjacency list
        for link in self.wn_pipes:
            # Check if link is a pipe
            if link['link_type'] != 'Pipe':
                # If link is not a pipe, skip it
                continue
            # Get start and end nodes
            start_node = link['start_node_name']
            end_node = link['end_node_name']
            # Check if start and end nodes are junctions
            if start_node not in self.junction_names or end_node not in self.junction_names:
                # If start or end node is not a junction, skip it
                continue
            # Get link name
            link_name = link['name']
            # Add start and end nodes to adjacency list
            if start_node not in self.adj_list:
                self.adj_list[start_node] = {}
            if end_node not in self.adj_list:
                self.adj_list[end_node] = {}
            # Add link to adjacency list
            self.adj_list[start_node][end_node] = {
                'link_name': link_name,
                'link_length': link['length']
                }
            self.adj_list[end_node][start_node] = {
                'link_name': link_name,
                'link_length': link['length']
            }
        return self.adj_list

    ### Getter methods ###
    # Method to get links and associated attributes
    def get_links(self):
        return self.wn_links

    # Method to get link link_names
    def get_link_names(self):
        return self.wn.link_name_list

    # Method to get nodes and associated attributes
    def get_nodes(self):
        return self.wn_nodes

    # Method to get node link_names
    def get_node_names(self):
        return self.wn.node_name_list

    # Method to get number of nodes
    def get_number_of_nodes(self):
        return len(self.get_node_names())

    # Method to get list of pipes - subtype of links
    def get_pipes(self):
        return self.wn_pipes

    # Method to get list of pipe link_names
    def get_pipe_link_names(self):
        return self.link_names

    # Method to get list of pipe link_lengths
    def get_pipe_link_lengths(self):
        return self.link_lengths

    # Method to get list of junctions - subtype of nodes
    def get_junctions(self):
        return self.wn_junctions

    # Method to get list of junction link_names
    def get_junction_names(self):
        return self.junction_names

    # Method to get graph
    def get_graph(self):
        return self.graph

    # Method to get undirected graph
    def get_undirected_graph(self):
        return self.undirected_graph

    # Method to get neighbor nodes given a current node
    def get_neighbours(self, current_node):
        return list(self.adj_list[current_node].keys())

    # Method to get neighbot nodes using networkx
    def get_neighbours_nx(self, current_node):
        return list(self.undirected_graph.neighbors(current_node))

    # Method to get pipe name given a start node and end node
    def get_pipe_name(self, start_node, end_node):
        return self.adj_list[start_node][end_node]['link_name']

    # Method to get pipe length given a start node and end node
    def get_pipe_length(self, start_node, end_node):
        return self.adj_list[start_node][end_node]['link_length']
    
    ### End of Getter methods ###
    
    # Method to write adjacency list to file
    def write_adj_list(self, filename='adj_list.txt'):
        with open(filename, 'w') as f:
            f.write(str(self.adj_list))
            f.close()

    # Method to write water network model to json file
    def write_wn_json(self, filename='wn.json'):
        wntr.network.write_json(self.wn, filename)

    # Method to render water network model - inherit args from wntr.graphics.plot_network
    def render_network(self, **kwargs):
        wntr.graphics.plot_network(self.wn, **kwargs)
        plt.show()

    # Method to get the state of the network at a given node
    def get_state(self, current_node):
        """
        Method to get the state of the network at node level
        :return: state of the junction
        """
        return list(self.adj_list[current_node].keys())

    # Method to remove non-junction nodes from the network
    def remove_non_junction_nodes(self):
        """
        Method to remove non-junction nodes from the network
        :return: None
        """
        # Iterate through nodes and remove non-junction nodes
        for node in self.wn_nodes:
            if node['node_type'] != 'Junction':
                self.wn.remove_node(node['name'])

    # Method to remove non-pipe links from the network
    def remove_non_pipe_links(self):
        """
        Method to remove non-pipe links from the network
        :return: None
        """
        # Iterate through links and remove non-pipe links
        for link in self.wn_links:
            if link['link_type'] != 'Pipe':
                self.wn.remove_link(link['name'])

    # Method to clean the network (remove non-junction nodes and non-pipe links) 
    # and return as a new network
    # TODO: Fix this method
    def clean_network(self):
        """
        Method to clean the network (remove non-junction nodes and non-pipe links)
        :return: Cleaned water network model
        """
        # Create a copy of the water network model
        wn_clean = copy.deepcopy(self.wn)
        # Get link name list
        link_names = wn_clean.link_name_list
        # Get links
        links = wn_clean.links
        # Iterate over links and remove non-pipe links
        for link in links:
            pass
        # Get pipe name list
        pipe_names = wn_clean.pipe_name_list
        # Get node name list
        node_names = wn_clean.node_name_list
        # Get junction name list
        junction_names = wn_clean.junction_name_list
        pass