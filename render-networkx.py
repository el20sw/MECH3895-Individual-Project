import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

from src.network import Network

# create a network
net = Network('networks/Net1.inp')
wn = net._wn

# Get the data
df = pd.read_csv('results/simulation_20230210_154320/results.csv', index_col=0)
agent_ids = [col for col in df.columns if col not in ['turn', 'pct_explored']]

print(df)
print(agent_ids)

# Create NetworkX graph
G = wn.to_graph()
uG = G.to_undirected()
# Get node positions
node_pos = nx.get_node_attributes(uG, 'pos')
# Make all nodes blue
nx.set_node_attributes(uG, 'blue', 'color')

print(node_pos)

# nx.draw(uG, node_pos, with_labels=True)

# create agent type nodes
for agent_id in agent_ids:
    uG.add_node(agent_id, color='red', type='agent')
    
node_types = nx.get_node_attributes(uG, 'type')

print(node_types)

# filter out non-agent nodes
agent_nodes = [node for node in node_types if node_types[node] == 'agent']
env_nodes = [node for node in node_types if node_types[node] != 'agent']

print(agent_nodes)

# get the agents starting positions
agent_start_pos = {}
for agent_id in agent_ids:
    agent_node = str(df[agent_id][0])
    # get the node position
    agent_start_pos[agent_id] = node_pos[agent_node]
    
print(agent_start_pos)

# set the agents starting positions
nx.set_node_attributes(uG, agent_start_pos, 'pos')

# get the positions of all objects
all_pos = nx.get_node_attributes(uG, 'pos')
all_colors = nx.get_node_attributes(uG, 'color')

print(all_pos)
print(all_colors)

nx.set_node_attributes(uG, all_pos, 'pos') 
# set agent nodes to red
nx.set_node_attributes(uG, 'red', 'color')


# Initialise the figure - make it big enough to fit all nodes
fig = plt.figure(figsize=(10, 10))
# Draw background environment nodes
nx.draw_networkx_nodes(uG, all_pos, nodelist=env_nodes, node_color='blue', label='Environment Nodes')
# Draw agent nodes
nx.draw_networkx_nodes(uG, all_pos, nodelist=agent_nodes, node_color='red', label='Agent Nodes')
# Draw edges
nx.draw_networkx_edges(uG, all_pos)
# Draw labels - make labels to the right of the nodes if node label is environment node and to the left if it is an agent node
node_labels = {node: node for node in uG.nodes()}
env_node_labels = {node: node for node in uG.nodes() if node in env_nodes}
agent_node_labels = {node: node for node in uG.nodes() if node in agent_nodes}
nx.draw_networkx_labels(uG, all_pos, labels=env_node_labels, 
                        horizontalalignment='right', verticalalignment='top',
                        font_weight='bold'
                        )
nx.draw_networkx_labels(uG, all_pos, labels=agent_node_labels, 
                        horizontalalignment='left', verticalalignment='bottom', 
                        bbox=dict(facecolor='red', alpha=0.5), font_weight='bold'
                        )
# Draw legend
plt.legend()
plt.show()

# def animate(i):
#     # Redraw the graph
#     pos = nx.get_node_attributes(uG, 'pos')
#     nx.draw(uG, pos, with_labels=True)


# ani = FuncAnimation(plt.gcf(), animate, frames=100, repeat=False)
