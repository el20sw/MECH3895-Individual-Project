from src.pipe_network import PipeNetwork
from random_agent import RandomAgent

import numpy as np

path_to_file = 'networks/Net1.inp'

# Create PipeNetwork environment
env = PipeNetwork(path_to_file)

# Get the adjacency list
adj_list = env.get_adj_list()
junctions = list(adj_list.keys())

# Get the possible starting nodes
nodes = env.get_node_names()

# Get state
state = env.get_state(nodes[3])
print(state)

# Create agent
agent = SimpleAgent(env, 0, nodes[3])

# Get observation
observation = agent.get_observation(environment=env)
print(observation)

# Render the network
env.render_network(node_labels=True, link_labels=True)
