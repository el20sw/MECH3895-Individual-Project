"""
Class for rendering a simulation
"""

import matplotlib
matplotlib.use("module://matplotlib.backends.backend_agg")

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation, FFMpegWriter

from src.simulation import Simulation

class Render:
    
    def __init__(self, simulation: Simulation):
        
        # get the environment from the simulation
        self.env = simulation.environment
        self.env_wn = self.env.water_network_model
        
        # get the raw data associated with the simulation
        self.results_directory = simulation.overwatch.path_to_results_directory
        self.results_file_path = simulation.overwatch.path_to_results_file
        self.df = pd.read_csv(simulation.overwatch.path_to_results_file, index_col=0)
        
        # get the agent ids
        self.agent_ids = [col for col in self.df.columns if col not in ['turn', 'pct_explored']]
        
        # get the number of turns
        self.num_turns = len(self.df.index)
        
        # create an undirected networkx graph
        self.G = self.env_wn.to_graph().to_undirected()
        
        # get the node positions
        self.env_node_pos = nx.get_node_attributes(self.G, 'pos')
        
        # make all environmental nodes blue
        nx.set_node_attributes(self.G, 'blue', 'color')
        
        # create agent type nodes
        for agent_id in self.agent_ids:
            self.G.add_node(agent_id, color='red', type='agent')
            
        # get the node types
        node_types = nx.get_node_attributes(self.G, 'type')
        
        # filter out non-agent nodes
        self.agent_nodes = [node for node in node_types if node_types[node] == 'agent']
        self.env_nodes = [node for node in node_types if node_types[node] != 'agent']
        
        # get the agents starting positions
        self.agent_start_pos = {}
        for agent_id in self.agent_ids:
            agent_node = str(self.df[agent_id][0])
            # get the node position
            self.agent_start_pos[agent_id] = self.env_node_pos[agent_node]
            
        # set the agents starting positions
        nx.set_node_attributes(self.G, self.agent_start_pos, 'pos')
        
        # get the positions of all objects
        self.all_pos = nx.get_node_attributes(self.G, 'pos')
        nx.set_node_attributes(self.G, self.all_pos, 'pos')
        
        # initialise the figure
        self.fig = plt.figure(figsize=(10, 10), dpi=100, facecolor='w', edgecolor='k')
        
        # draw the network nodes
        nx.draw_networkx_nodes(self.G, self.all_pos, nodelist=self.env_nodes, node_color='blue', label='Environmental Nodes')
        
        # draw the agent nodes
        nx.draw_networkx_nodes(self.G, self.all_pos, nodelist=self.agent_nodes, node_color='red', label='Agent Nodes')
        
        # draw the edges
        nx.draw_networkx_edges(self.G, self.env_node_pos)
        
        # draw the labels
        env_node_labels = {node: node for node in self.G.nodes() if node in self.env_nodes}
        agent_node_labels = {node: node for node in self.G.nodes() if node in self.agent_nodes}
        nx.draw_networkx_labels(
            self.G, self.all_pos, labels=env_node_labels, 
            horizontalalignment='right', verticalalignment='top',
            font_weight='bold'
            )
        nx.draw_networkx_labels(
            self.G, self.all_pos, labels=agent_node_labels, 
            horizontalalignment='left', verticalalignment='bottom', 
            bbox=dict(facecolor='red', alpha=0.5), font_weight='bold'
            )
        
    def animate(self, i):
        
        # check if i < num_turns
        if i >= self.num_turns:
            return
        # get the current turn - turns are the index of the dataframe
        turn = self.df.index[i]
        # get the current percentage explored
        pct_explored = self.df['pct_explored'][i]    
        # get the current positions of the agents
        agent_pos = {}
        for agent_id in self.agent_ids:
            agent_node = str(self.df[agent_id][i])
            # get the node position
            agent_pos[agent_id] = self.env_node_pos[agent_node]
            
        # update the positions of the agents
        nx.set_node_attributes(self.G, agent_pos, 'pos')
        # get the positions of all objects
        self.all_pos = nx.get_node_attributes(self.G, 'pos')
        # update the positions of all objects
        nx.set_node_attributes(self.G, self.all_pos, 'pos')
        # update the figure
        self.fig.clear()
        
        # Draw background environment nodes
        nx.draw_networkx_nodes(self.G, self.all_pos, nodelist=self.env_nodes, node_color='blue', label='Environment Nodes')
        # Draw agent nodes
        nx.draw_networkx_nodes(self.G, self.all_pos, nodelist=self.agent_nodes, node_color='red', label='Agent Nodes')
        # Draw edges
        nx.draw_networkx_edges(self.G, self.all_pos)
        
        # Draw labels - make labels to the right of the nodes if node label is environment node and to the left if it is an agent node
        env_node_labels = {node: node for node in self.G.nodes() if node in self.env_nodes}
        agent_node_labels = {node: node for node in self.G.nodes() if node in self.agent_nodes}
        # Draw labels
        nx.draw_networkx_labels(self.G, self.all_pos, labels=env_node_labels,
                                horizontalalignment='right', verticalalignment='top',
                                font_weight='bold'
                                )
        nx.draw_networkx_labels(self.G, self.all_pos, labels=agent_node_labels,
                                horizontalalignment='left', verticalalignment='bottom',
                                bbox=dict(facecolor='red', alpha=0.5), font_weight='bold'
                                )

        # Add title
        plt.title('Turn: {} - {}% explored'.format(turn, pct_explored))
        
        # Add title
        plt.title('Turn: {} - {}% explored'.format(turn, pct_explored)) 
    

    def render(self, frames=None, repeat=False, interval=500):
        """
        Function to render a simulation
        :param simulation: Simulation object
        """
        
        if frames is None:
            frames = self.num_turns + 1
        # create animation object
        writervideo = FFMpegWriter(fps=1)
        animation = FuncAnimation(plt.gcf(), self.animate, frames=frames, repeat=repeat, interval=interval)
        animation_loc = f'{self.results_directory}/animation.mp4'
        animation.save(animation_loc, writer=writervideo)
        plt.close()
    
