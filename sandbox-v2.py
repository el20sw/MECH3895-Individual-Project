import wntr
import networkx as nx
import matplotlib.pyplot as plt

import math

# from matplotlib.animation import FuncAnimation

import src.debug.logger as logger
from src.agent import Agent
from src.network import Network
import src.agent_generator as agent_generator
import src.communication as communication

from src.simulation import Simulation
from src.render import Render

# import tkinter as tk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure



# log = logger.setup_logger(file_name='logs/sandbox-2.log', level='DEBUG')

# env = Network('networks/Net1.inp')
# wn = env.water_network_model
# g = wn.to_graph()
# uG = g.to_undirected()

# adj = env.adj_list

# sim = Simulation(environment=env, num_agents=20, swarm=True)
# sim.turn()
# sim.turn()

agents = [1, 2, 3, 4]
ports = ['a', 'b', 'c', 'd', 'e']
arrival_ports = {1: 'a', 2: 'a', 3: 'b', 4: 'c'}
next_ports = {1: 'b', 2: 'b', 3: 'c', 4: 'd'}
port_scores = {}
assignment_port_scores = {port: 0 for port in ports}

for port in ports:
    # if port is an arrival port, add the number of agents that arrived at that port to the port score else score is 0
    if port in arrival_ports.values():
        port_scores.update({port: len([agent for agent in arrival_ports if arrival_ports[agent] == port])})
    else:
        port_scores.update({port: 0})
        
    # if the port is a next port (according to RH-traversal), add the number of agents that are going to that port to the port score
    if port in next_ports.values():
        assignment_port_scores[port] += len([agent for agent in next_ports if next_ports[agent] == port])

print(port_scores)
total_port_score = sum(port_scores.values())
print(total_port_score)

print(assignment_port_scores)

# The leader should aim to assign agents that are redundant (that is doubled up) with priority given to ports with the lowest scores
redundant_agents = [port for port in assignment_port_scores if assignment_port_scores[port] > 1]
number_agents_to_assign = len(redundant_agents)
print(redundant_agents)
print(number_agents_to_assign)