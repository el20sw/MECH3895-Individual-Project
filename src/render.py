"""
Class for rendering a simulation as an animation - uses matplotlib and networkx to render the simulation and save it as a video file using ffmpeg
"""

import matplotlib
# matplotlib.use("module://matplotlib.backends.backend_agg")

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation, FFMpegWriter

from src.simulation import Simulation

class Render:
    """
    Render Class
    =================
    
    Render a given simulation as an animation
    
    Parameters
    ----------
    
    Simulation: Simulation
        The simulation to render
        
    Description
    -----------
    
    The Render class is used to render a given simulation as an animation. It uses matplotlib and networkx to render the simulation and save it as a video file using ffmpeg.
    Agents are represented as red nodes and environmental nodes are represented as blue nodes. Each turn is represented as a frame in the animation, and agents move from node to node as they explore the environment.
    
    """

    def __init__(self, simulation: Simulation):

        # get the environment from the simulation
        self.env = simulation.environment
        self.env_wn = self.env.water_network_model
        self.num_nodes = len(self.env_wn.nodes)

        # get the raw data associated with the simulation
        self.results_directory = simulation.path_to_results_directory
        self.results_file_path = simulation.path_to_results_file
        self.agents_results_file_path = simulation.path_to_agents_results_file
        self.results_df = pd.read_csv(simulation.path_to_results_file, index_col=0)
        self.agents_results_df = pd.read_csv(simulation.path_to_agents_results_file)
        
        # get the agent ids
        self.agent_ids = [agent.agent_id for agent in simulation.agents]

        # get the number of turns
        self.num_turns = len(self.results_df.index)
        # sanity check that number of turns is the same
        if simulation.turns != self.num_turns:
            raise ValueError('Number of turns in simulation and results do not match')

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
            agent_node = str(self.agents_results_df['start_pos'][agent_id])
            # get the node position
            self.agent_start_pos[agent_id] = self.env_node_pos[agent_node]

        # set the agents starting positions
        nx.set_node_attributes(self.G, self.agent_start_pos, 'pos')

        # get the positions of all objects
        self.all_pos = nx.get_node_attributes(self.G, 'pos')
        nx.set_node_attributes(self.G, self.all_pos, 'pos')

        # initialise the figure
        fig = plt.figure(figsize=(10, 10), dpi=100, facecolor='w', edgecolor='k')
        self.plot = fig.add_subplot(111)

        # draw the network nodes
        nx.draw_networkx_nodes(self.G, self.all_pos, nodelist=self.env_nodes, node_color='blue', node_size=10, label='Environmental Nodes')

        # draw the agent nodes
        nx.draw_networkx_nodes(self.G, self.all_pos, nodelist=self.agent_nodes, node_color='red', node_size=10, label='Agent Nodes')

        # draw the edges
        nx.draw_networkx_edges(self.G, self.env_node_pos)

        # draw the environment labels if the number of nodes is less than 300
        if self.num_nodes < 300:
            self.draw_env_labels()
        # always draw the agent labels
        agent_node_labels = {node: node for node in self.G.nodes() if node in self.agent_nodes}  
        nx.draw_networkx_labels(self.G, self.all_pos, labels=agent_node_labels,
                                horizontalalignment='center', verticalalignment='center',
                                bbox=dict(facecolor='red', alpha=0.5), font_family='sans-serif', font_size=10
                                )
        
    def draw_env_labels(self):
        """
        Method for drawing the labels
        """
        
        # draw the labels
        env_node_labels = {node: node for node in self.G.nodes() if node in self.env_nodes}
        
        nx.draw_networkx_labels(
            self.G, self.all_pos, labels=env_node_labels,
            horizontalalignment='right', verticalalignment='top',
            font_family='sans-serif', font_size=8
            )

    def animate(self, i):

        # check if i < num_turns
        if i >= self.num_turns:
            return
        # get the current turn - turns are the index of the dataframe
        turn = self.results_df.index[i]
        # get the current percentage explored
        pct_nodes_explored = self.results_df['pct_nodes_explored'][i]
        pct_links_explored = self.results_df['pct_links_explored'][i]
        
        # get the current positions of the agents
        agent_pos = {}
        for agent_id in self.agent_ids:
            agent_path = self.agents_results_df['path'][agent_id].strip('[]').split(',')
            for j in range(len(agent_path)):
                agent_path[j] = agent_path[j].strip().strip("'")
            agent_node = agent_path[turn]
            agent_pos[agent_id] = self.env_node_pos[agent_node]

        # update the positions of the agents
        nx.set_node_attributes(self.G, agent_pos, 'pos')
        # get the positions of all objects
        self.all_pos = nx.get_node_attributes(self.G, 'pos')
        # update the positions of all objects
        nx.set_node_attributes(self.G, self.all_pos, 'pos')
        # update the figure
        self.plot.clear()

        # Draw background environment nodes
        nx.draw_networkx_nodes(self.G, self.all_pos, nodelist=self.env_nodes, node_color='blue', node_size=10, label='Environment Nodes')
        # Draw agent nodes
        nx.draw_networkx_nodes(self.G, self.all_pos, nodelist=self.agent_nodes, node_color='red', node_size=10, label='Agent Nodes')
        # Draw edges
        nx.draw_networkx_edges(self.G, self.all_pos)

        # Draw environment labels if the number of nodes is less than 300
        if self.num_nodes < 300:
            self.draw_env_labels()
        # always draw the agent labels
        agent_node_labels = {node: node for node in self.G.nodes() if node in self.agent_nodes}  
        nx.draw_networkx_labels(self.G, self.all_pos, labels=agent_node_labels,
                                horizontalalignment='center', verticalalignment='center',
                                bbox=dict(facecolor='red', alpha=0.5), font_family='sans-serif', font_size=10
                                )

        # Add title with pct explored to 2 decimal places
        plt.title('Turn: {} - {}% Nodes explored - {}% Links explored'.format(turn, round(pct_nodes_explored, 2), round(pct_links_explored, 2)))
        # plt.title('Turn: {} - {}% explored'.format(turn, pct_explored))


    def render(self, frames=None, repeat=False, interval=250):
        """
        Function to render a simulation
        
        Parameters
        ----------
        frames : int, optional
            The number of frames to render, by default None
        repeat : bool, optional
            Whether to repeat the animation, by default False
        interval : int, optional
            The interval between frames in milliseconds, by default 250
            
        Description
        ------------
        
        Uses the matplotlib animation library to render the simulation and write it to a video file.
        
        """

        if frames is None:
            frames = self.num_turns + 1
        # create animation object
        writervideo = FFMpegWriter(fps=1)
        animation = FuncAnimation(plt.gcf(), self.animate, frames=frames, repeat=repeat, interval=interval)
        animation_loc = f'{self.results_directory}/animation.mp4'
        animation.save(animation_loc, writer=writervideo)
        plt.close()

