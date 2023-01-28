### Import modules
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
        
        
        self.adj_list = {}

    # Get adjacency list
    def get_adj_list(self):
        """
        Method to get adjacency list - filters out non-pipe links
        :return: Adjacency list
        """
        # Iterate through links and add start_node to adjacency list and end_node to adjacency list
        for link in self.wn_pipes:
            # Check if link is a pipe
            # TODO: Reinstate this check?
            # if link['link_type'] != 'Pipe':
            #     # If link is not a pipe, skip it
            #     continue
            # Get start and end nodes
            start_node = link['start_node_name']
            end_node = link['end_node_name']
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

    # Method to get list of junctions - subtype of nodes
    def get_junctions(self):
        return self.wn_junctions

    # Method to get graph
    def get_graph(self):
        return self.graph

    # Method to get undirected graph
    def get_undirected_graph(self):
        return self.undirected_graph

    # Method to get list of pipe link_names
    def get_pipe_link_names(self):
        return self.link_names

    # Method to get list of pipe link_lengths
    def get_pipe_link_lengths(self):
        return self.link_lengths

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
        wntr.network.to_json(self.wn, filename)

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
        