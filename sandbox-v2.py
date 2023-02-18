import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import src.debug.logger as logger
from src.agent import Agent
from src.network import Network

SIM_LENGTH = 1000

log = logger.setup_logger(file_name='logs/sandbox-2.log', level='DEBUG')

env = Network('networks/Net3.inp')
print(env.node_names)
agent = Agent(env=env, agent_id=0x1, start_pos='10')


G = env.water_network_model.to_graph().to_undirected()

num_nodes = len(G.nodes)
pct_explored = 0
visited_nodes = set()
log.info(f'num_nodes: {num_nodes}')
log.info(f'pct_explored: {pct_explored}')

while pct_explored < 1:
    if SIM_LENGTH == 0:
        print('Simulation length exceeded')
        break
    
    visited_nodes.add(agent.position)
    pct_explored = len(visited_nodes) / num_nodes
    log.info(f'pct_explored: {pct_explored}')
    agent.RH_Traversal()
    agent.move()
    SIM_LENGTH -= 1
    
path = agent.path
num_frames = len(path)
node_pos = nx.get_node_attributes(G, 'pos')

# create a figure
plt.figure(figsize=(10, 10))
# draw the network
nx.draw_networkx_nodes(G, node_pos, node_size=10, node_color='blue')
nx.draw_networkx_edges(G, node_pos)
nx.draw_networkx_labels(G, node_pos, horizontalalignment='right', verticalalignment='top', font_family='serif', font_size=8)

def animate(i):
    if i == 0:
        nx.draw_networkx_nodes(G, node_pos, node_size=10, node_color='blue')
    
    visited_nodes = []
    node = path[i]
    visited_nodes.append(node)
    
    nx.draw_networkx_nodes(G, node_pos, nodelist=[node], node_size=15, node_color='red')
    if i > 0:
        prev_node = path[i-1]
        nx.draw_networkx_nodes(G, node_pos, nodelist=[prev_node], node_size=10, node_color='lightgreen')
        
    plt.title(f'Frame: {i} / {num_frames} ({round(i/num_frames*100, 2)}%)')
    
anim = FuncAnimation(plt.gcf(), animate, frames=num_frames, interval=100)
plt.show()