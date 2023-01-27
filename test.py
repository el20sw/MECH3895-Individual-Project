from src.pipe_network import PipeNetwork
from simple_agent import SimpleAgent

import numpy as np

path_to_file = 'networks/Net1.inp'

# Create PipeNetwork environment
env = PipeNetwork(path_to_file)

# Get the adjacency list
adj_list = env.get_adj_list()
junctions = list(adj_list.keys())

# Get state
state = env.get_state(junctions[3])
print(state)

# Get nodes
nodes = env.get_node_names()
print(nodes)

# Create agent
agent = SimpleAgent(env, 0, junctions[3])

# Render the network
env.render_network(node_labels=True, link_labels=True)
