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

        # draw the labels
        env_node_labels = {node: node for node in self.G.nodes() if node in self.env_nodes}
        agent_node_labels = {node: node for node in self.G.nodes() if node in self.agent_nodes}
        nx.draw_networkx_labels(
            self.G, self.all_pos, labels=env_node_labels,
            horizontalalignment='right', verticalalignment='top',
            font_family='sans-serif', font_size=8
            )
        
    #     fig.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)
        
    # def on_plot_hover(self, event):
    #     # Iterate over each data point in the plot
    #     for curve in self.plot.get_lines():
    #         if curve.contains(event)[0]:
    #             # If the mouse is over the data point, display the corresponding label
    #             self.plot.set_title(curve.get_label())
    #             # Force a redraw of the figure
    #             self.plot.figure.canvas.draw()

    def animate(self, i):

        # check if i < num_turns
        if i >= self.num_turns:
            return
        # get the current turn - turns are the index of the dataframe
        turn = self.results_df.index[i]
        # get the current percentage explored
        pct_explored = self.results_df['pct_explored'][i]
        
        # get the current positions of the agents
        agent_pos = {}
        for agent_id in self.agent_ids:
            agent_path = self.agents_results_df['path'][agent_id].strip('[]').split(',')
            for j in range(len(agent_path)):
                agent_path[j] = agent_path[j].strip().strip("'")
            agent_node = agent_path[turn]
            agent_pos[agent_id] = self.env_node_pos[agent_node]
            
        
            
            
        
        
        # agent_pos = {}
        # for agent_id in self.agent_ids:
        #     agent_node = str(self.results_df[agent_id][i])
        #     # get the node position
        #     agent_pos[agent_id] = self.env_node_pos[agent_node]
        
        # if i != 0:
        #     # get a list of the visited nodes at that turn
        #     with open(self.visited_nodes_file_path, 'r') as vnodes_file:
        #         # get the line corresponding to the current turn
        #         if i == self.num_turns - 1:
        #             line = vnodes_file.readlines()[i-2]
        #         else:
        #             line = vnodes_file.readlines()[i]
        #         # remove the turn number and newline character
        #         fline = line.lstrip(f'{str(i+1)}:').rstrip('\n')
        #         # split the line into a list of visited nodes
        #         visited_nodes = fline.split(',')
        #         # close the file
        #         vnodes_file.close()
        # else:
        #     visited_nodes = []

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

        # Draw labels - make labels to the right of the nodes if node label is environment node and to the left if it is an agent node
        env_node_labels = {node: node for node in self.G.nodes() if node in self.env_nodes}
        agent_node_labels = {node: node for node in self.G.nodes() if node in self.agent_nodes}
        # Draw labels
        nx.draw_networkx_labels(self.G, self.all_pos, labels=env_node_labels,
                                horizontalalignment='right', verticalalignment='top',
                                font_weight='bold', font_size=10
                                )
        nx.draw_networkx_labels(self.G, self.all_pos, labels=agent_node_labels,
                                horizontalalignment='center', verticalalignment='center',
                                bbox=dict(facecolor='red', alpha=0.5), font_family='sans-serif', font_size=10
                                )

        # Add title with pct explored to 2 decimal places
        plt.title('Turn: {} - {}% explored'.format(turn, round(pct_explored, 2)))
        # plt.title('Turn: {} - {}% explored'.format(turn, pct_explored))


    def render(self, frames=None, repeat=False, interval=250):
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

