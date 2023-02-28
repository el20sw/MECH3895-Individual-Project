import wntr
import networkx as nx
import matplotlib.pyplot as plt

import math

from matplotlib.animation import FuncAnimation

import src.debug.logger as logger
from src.agent import Agent
from src.network import Network
import src.agent_generator as agent_generator
import src.communication as communication

from src.simulation import Simulation
from src.render import Render

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

log = logger.setup_logger(file_name='logs/sandbox-2.log', level='DEBUG')

env = Network('networks/Net6.inp')

wn = env.water_network_model
g = wn.to_graph().to_undirected()

adj = wn.to_dict()

# print(env.adj_list)
# print("Link 10 -> 11: ", env.get_link('10', '11'))
# print("Links @ 22: ", env.get_links('22'))
# print("Node from node 31 and link 31: ", env.get_node('31', '31'))

# def calculate_link_length(wn, start_node, end_node) -> float:
#         """
#         :py:meth:`calculate_link_length` is a :py:class:`float` method to calculate the length of a link given the coordinates of the start and end nodes
#         """
#         # Get coordinates of start and end nodes
#         start_node = wn.get_node(start_node)
#         end_node = wn.get_node(end_node)
#         # try to get the coordinates
#         start_node_coords = getattr(start_node, 'coordinates', None)
#         end_node_coords = getattr(end_node, 'coordinates', None)
#         # If the coordinates are not None, calculate the length of the link
#         if start_node_coords is not None and end_node_coords is not None:
#             return math.sqrt((start_node_coords[0] - end_node_coords[0])**2 + (start_node_coords[1] - end_node_coords[1])**2)
#         # If the coordinates are None, return 10
#         else:
#             return 10

# def to_graph(wn):
#     uG = nx.Graph()
    
#     for name, node in wn.nodes():
#         uG.add_node(name)
#         nx.set_node_attributes(uG, name="pos", values={name: node.coordinates})
#         nx.set_node_attributes(uG, name="type", values={name: node.node_type})
        
#     for name, link in wn.links():
#         start_node = link.start_node_name
#         end_node = link.end_node_name
        
#         uG.add_edge(start_node, end_node)
        
#         nx.set_edge_attributes(uG, name="link_name", values={(start_node, end_node): name})
        
#         try:
#             nx.set_edge_attributes(uG, name="link_length", values={(start_node, end_node): link.length})
#         except AttributeError:
#             length = calculate_link_length(wn, start_node, end_node)
#             nx.set_edge_attributes(uG, name="link_length", values={(start_node, end_node): length})
      
#     return uG.to_undirected()

# uG = to_graph(wn)
# print(nx.is_connected(uG))
# print(uG.adj)

sim = Simulation(environment=env, num_agents=1, swarm=True)

# wn = env.water_network_model
# g = wn.to_graph().to_undirected()

# # check that the graph is connected
# if not nx.is_connected(g):
#     raise ValueError('Graph is not connected')

sim.turn()
sim.turn()
    






# SIM_LENGTH = 200

# log = logger.setup_logger(file_name='logs/sandbox-2.log', level='DEBUG')

# env = Network('networks/Net3.inp')
# g = env.water_network_model.to_graph().to_undirected()
# pos = nx.get_node_attributes(g, "pos")

# root = tk.Tk()
# root.title("Select Starting Positions")

# # Make a base canvas
# base = tk.Canvas(root, width=800, height=800)
# base.pack()

# fig = Figure(figsize=(10, 10), dpi=100)
# ax = fig.add_subplot(111)
# nx.draw_networkx_nodes(g, pos=pos, node_size=5, ax=ax)
# nx.draw_networkx_edges(g, pos=pos, ax=ax)

# # Create a Matplotlib canvasjyy
# canvas = FigureCanvasTkAgg(fig, master=base)
# canvas.draw()
# canvas.get_tk_widget().pack()

# Make option to zoom in and out


# Make nodes change color when clicked
# def on_click(event):
#     x, y = event.x, event.y
#     for node in g.nodes:
#         node_coords = pos[node] 
#         node_x, node_y = node_coords
#         if node_x - 5 <= x <= node_x + 5 and node_y - 5 <= y <= node_y + 5:
#             canvas.itemconfig(node, fill="red", outline="red")

# Run the Tkinter event loop
# tk.mainloop()


# class StartingPositionsGUI:
#     def __init__(self, environment:Network) -> None:
#         self.env = environment
#         self.starting_positions = []
        
#         self.G = self.env.water_network_model.to_graph().to_undirected()
#         self.node_names = self.env.node_names
        
#         self.window = tk.Tk()
#         self.window.title("Select Starting Positions")
#         self.canvas = tk.Canvas(self.window, width=800, height=800)
#         self.canvas.pack()
#         self.canvas.bind("<Button-1>", self.on_click)
        
#         self.nodes = []
#         self.all_pos = nx.get_node_attributes(self.G, "pos")
        
#         for node in self.node_names:
#             node_coords = self.all_pos[node]
#             node_x, node_y = node_coords
#             node_radius = 5
#             node_color = "blue"
#             node_id = self.canvas.create_oval(
#                 node_x - node_radius,
#                 node_y - node_radius,
#                 node_x + node_radius,
#                 node_y + node_radius,
#                 fill=node_color,
#                 outline=node_color,
#             )
#             self.nodes.append(node_id)  
            
#         self.start_button = tk.Button(self.window, text="Start", command=self.start)
#         self.start_button.pack()
    
#     def on_click(self, event):
#         x, y = event.x, event.y
#         for node_id in self.nodes:
#             node_coords = self.canvas.coords(node_id)
#             if node_coords[0] <= x <= node_coords[2] and node_coords[1] <= y <= node_coords[3]:
#                 node_index = self.nodes.index(node_id)
#                 self.starting_positions.append(node_index)
#                 self.canvas.itemconfig(node_id, fill="green")
                
#     def start(self):
#         if len(self.starting_positions) > 0:
#             self.window.destroy()

#     def get_starting_positions(self):
#         return [node for node in self.starting_positions]
    
# starting_positions_gui = StartingPositionsGUI(env)
# starting_positions_gui.window.mainloop()
# starting_positions = starting_positions_gui.get_starting_positions()


































   
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
