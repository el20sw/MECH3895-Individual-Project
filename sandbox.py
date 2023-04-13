import wntr
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import src.debug.logger as logger
from src.agent import Agent
from src.network import Network
import src.agent_generator as agent_generator
import src.communication as communication

from src.simulation import Simulation
from src.render import Render

SIM_LENGTH = 200

log = logger.setup_logger(file_name='logs/sandbox-2.log', level='CRITICAL')

path = "networks/Net1.inp"
env = Network(path)
file = 'notable-results/Iteration3/no-swarm-validation'
sim = Simulation(env, num_agents=1, swarm=False, start_positions=['9'], filepath=file)
sim.run(max_turns=20)
r = Render(sim)
r.render()

spath = sim.path_to_results_directory

# Plot the path of the agent over time in a static graph
agent = sim.agents[0]
npath = agent.node_path

links = []
for i in range(len(npath)-1):
    links.append((npath[i], npath[i+1]))
    
pos = nx.get_node_attributes(env.graph, 'pos')

# create a figure
plt.figure(figsize=(10, 10))
# draw the network
nx.draw_networkx_nodes(env.graph, pos, node_size=1, node_color='blue')
nx.draw_networkx_edges(env.graph, pos)
nx.draw_networkx_labels(env.graph, pos, horizontalalignment='right', verticalalignment='top', font_family='serif', font_size=8)
# draw the path
nx.draw_networkx_nodes(env.graph, pos, nodelist=npath, node_size=10, node_color='red')
nx.draw_networkx_edges(env.graph, pos, edgelist=links, edge_color='red', width=2)

# add a title
plt.title('Agent Path for Base Behavior (RH Traversal)')

plt.savefig(f'{spath}/agent_path.png')



# path1 = "networks/250701 K709vs2-Export.inp"
# path2 = "networks/Net6.inp"
# env = Network(path1)

# sim = Simulation(env, num_agents=100, swarm=True, swarm_config={'swarm': True, 'swarm_type': 'informed', 'allocation_threshold': 'mean'}, start_positions=['A2148'])
# sim.run(max_turns=100)

# nn = sim._num_nodes
# gn = sim._graph_num_nodes

# nl = sim._num_links
# gl = sim._graph_num_links

# print(f'num_nodes: {nn}, graph_num_nodes: {gn}')
# print(f'num_links: {nl}, graph_num_links: {gl}')

# r = Render(sim)
# r.render()


# print(sim.pct_nodes_explored)
# print(sim.pct_links_explored)
# r = Render(sim)
# r.render()

# agent = Agent(env=env, agent_id=0x1, start_pos='Lake')

# wn = env.water_network_model
# G = wn.to_graph().to_undirected()

# sim = Simulation(env, num_agents=5, swarm=True)

# sim.run(max_turns=100)

# render = Render(sim)
# render.render()

# sim.agents[0]._current_node = '10'
# sim.agents[1]._current_node = '10'
# sim.agents[2]._current_node = '10'

# sim.agents[3]._current_node = '113'
# sim.agents[4]._current_node = '113'
# sim.agents[5]._current_node = '113'

# sim.agents[6]._current_node = '197'

# log.critical(f'Communication state\n')
# sim.comms_state()
# log.critical(f'Decide state\n')
# sim.decide_state()
# log.critical(f'Action state\n')
# sim.action_state()

# num_nodes = len(G.nodes)
# pct_explored = 0
# visited_nodes = set()
# log.info(f'num_nodes: {num_nodes}')
# log.info(f'pct_explored: {pct_explored}')

# while pct_explored < 1:
#     if SIM_LENGTH == 0:
#         print('Simulation length exceeded')
#         break

#     visited_nodes.add(agent.position)
#     pct_explored = len(visited_nodes) / num_nodes
#     log.info(f'pct_explored: {pct_explored}')
#     agent.RH_Traversal()
#     agent.move()
#     SIM_LENGTH -= 1

# path = agent.path
# num_frames = len(path)
# node_pos = nx.get_node_attributes(G, 'pos')

# # create a figure
# plt.figure(figsize=(10, 10))
# # draw the network
# nx.draw_networkx_nodes(G, node_pos, node_size=10, node_color='blue')
# nx.draw_networkx_edges(G, node_pos)
# nx.draw_networkx_labels(G, node_pos, horizontalalignment='right', verticalalignment='top', font_family='serif', font_size=8)

# def animate(i):
#     if i == 0:
#         nx.draw_networkx_nodes(G, node_pos, node_size=10, node_color='blue')

#     visited_nodes = []
#     node = path[i]
#     visited_nodes.append(node)

#     nx.draw_networkx_nodes(G, node_pos, nodelist=[node], node_size=15, node_color='red')
#     if i > 0:
#         prev_node = path[i-1]
#         nx.draw_networkx_nodes(G, node_pos, nodelist=[prev_node], node_size=10, node_color='lightgreen')

#     plt.title(f'Frame: {i} / {num_frames} ({round(i/num_frames*100, 2)}%)')

# anim = FuncAnimation(plt.gcf(), animate, frames=num_frames, interval=100)
# plt.show()
