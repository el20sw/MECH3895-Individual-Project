import wntr
import networkx as nx
import matplotlib.pyplot as plt

import math
import copy

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



log = logger.setup_logger(file_name='logs/sandbox-2.log', level='DEBUG')

env = Network('networks/Net1.inp')
# wn = env.water_network_model
# g = wn.to_graph()
# uG = g.to_undirected()

# adj = env.adj_list

sim = Simulation(environment=env, num_agents=10, swarm=True)
sim.turn()
sim.turn()

# agents = [1, 2, 3, 4]
# ports = ['a', 'b', 'c', 'd', 'e']
# arrival_ports = {1: 'a', 2: 'a', 3: 'b', 4: 'c'}
# next_ports = {1: 'b', 2: 'b', 3: 'c', 4: 'd'}
# port_scores = {}
# assignment_port_scores = {port: 0 for port in ports}

# for port in ports:
#     # if port is an arrival port, add the number of agents that arrived at that port to the port score else score is 0
#     if port in arrival_ports.values():
#         port_scores.update({port: len([agent for agent in arrival_ports if arrival_ports[agent] == port])})
#     else:
#         port_scores.update({port: 0})
        
#     # if the port is a next port (according to RH-traversal), add the number of agents that are going to that port to the port score
#     if port in next_ports.values():
#         assignment_port_scores[port] += len([agent for agent in next_ports if next_ports[agent] == port])

# # print(port_scores)
# # total_port_score = sum(port_scores.values())
# # print(total_port_score)

# # print(assignment_port_scores)

# def mean_assignment(mean_port_score, sorted_port_scores, agents):
    
#     assignments = {agent: None for agent in agents}
    
#     # If the port score is less than the mean port score, the port is considered to be underutilized
#     mean_underutilized_ports = [port for port, score in port_scores.items() if score < mean_port_score]
#     print(f'Underutilized ports: {mean_underutilized_ports}')
    
#     # If the port score is greater than the mean port score, the port is considered to be overutilized
#     mean_overutilized_ports = [port for port, score in port_scores.items() if score > mean_port_score]
#     print(f'Overutilized ports: {mean_overutilized_ports}')
    
#     # If the port score is equal to the mean port score, the port is considered to be balanced
#     mean_balanced_ports = [port for port, score in port_scores.items() if score == mean_port_score]
#     print(f'Balanced ports: {mean_balanced_ports}')
    
#     # Priority 1: Assign agents to underutilized ports
#     if len(mean_underutilized_ports) > 0:
#         log.info(f'Underutilized ports: {mean_underutilized_ports}')
#         # If there are underutilized ports, assign agents to the underutilized ports
#         for port in mean_underutilized_ports:
#             # If there are agents available, assign them to the port
#             if len(agents) > 0:
#                 agent = agents.pop(0)
#                 assignments.update({agent: port})
#                 print(f'Agent {agent} assigned to port {port}')
#             else:
#                 print('No agents available')
                
#     # Priority 2: Assign agents to balanced ports
#     if len(mean_balanced_ports) > 0:
#         log.info(f'Balanced ports: {mean_balanced_ports}')
#         # If there are balanced ports, assign agents to the balanced ports
#         for port in mean_balanced_ports:
#             # If there are agents available, assign them to the port
#             if len(agents) > 0:
#                 agent = agents.pop(0)
#                 assignments.update({agent: port})
#                 print(f'Agent {agent} assigned to port {port}')
#             else:
#                 print('No agents available')
                
#     # Priority 3: Assign agents to overutilized ports
#     if len(mean_overutilized_ports) > 0:
#         log.info(f'Overutilized ports: {mean_overutilized_ports}')
#         # If there are overutilized ports, assign agents to the overutilized ports
#         for port in mean_overutilized_ports:
#             # If there are agents available, assign them to the port
#             if len(agents) > 0:
#                 agent = agents.pop(0)
#                 assignments.update({agent: port})
#                 print(f'Agent {agent} assigned to port {port}')
#             else:
#                 print('No agents available')
                
#     # If there are still agents available, assign them to the port with the lowest score
#     if len(agents) > 0:
#         log.info(f'Agents available: {agents}')
#         for agent in agents:
#             port = sorted_port_scores[0][0]
#             assignments.update({agent: port})
#             print(f'Agent {agent} assigned to port {port}')
            
#     return assignments

# def median_assignment(median_port_score, sorted_port_scores, agents):
    
#     assignments = {agent: None for agent in agents}
    
#     # If the port score is less than the median port score, the port is considered to be underutilized
#     median_underutilized_ports = [port for port, score in port_scores.items() if score < median_port_score]
#     print(f'Underutilized ports: {median_underutilized_ports}')
    
#     # If the port score is greater than the median port score, the port is considered to be overutilized
#     median_overutilized_ports = [port for port, score in port_scores.items() if score > median_port_score]
#     print(f'Overutilized ports: {median_overutilized_ports}')
    
#     # If the port score is equal to the median port score, the port is considered to be balanced
#     median_balanced_ports = [port for port, score in port_scores.items() if score == median_port_score]
#     print(f'Balanced ports: {median_balanced_ports}')
    
#     # Priority 1: Assign agents to underutilized ports
#     if len(median_underutilized_ports) > 0:
#         log.info(f'Underutilized ports: {median_underutilized_ports}')
#         # If there are underutilized ports, assign agents to the underutilized ports
#         for port in median_underutilized_ports:
#             # If there are agents available, assign them to the port
#             if len(agents) > 0:
#                 agent = agents.pop(0)
#                 assignments.update({agent: port})
#                 print(f'Agent {agent} assigned to port {port}')
#             else:
#                 print('No agents available')
                
#     # Priority 2: Assign agents to balanced ports
#     if len(median_balanced_ports) > 0:
#         log.info(f'Balanced ports: {median_balanced_ports}')
#         # If there are balanced ports, assign agents to the balanced ports
#         for port in median_balanced_ports:
#             # If there are agents available, assign them to the port
#             if len(agents) > 0:
#                 agent = agents.pop(0)
#                 assignments.update({agent: port})
#                 print(f'Agent {agent} assigned to port {port}')
#             else:
#                 print('No agents available')
                
#     # Priority 3: Assign agents to overutilized ports
#     if len(median_overutilized_ports) > 0:
#         log.info(f'Overutilized ports: {median_overutilized_ports}')
#         # If there are overutilized ports, assign agents to the overutilized ports
#         for port in median_overutilized_ports:
#             # If there are agents available, assign them to the port
#             if len(agents) > 0:
#                 agent = agents.pop(0)
#                 assignments.update({agent: port})
#                 print(f'Agent {agent} assigned to port {port}')
#             else:
#                 print('No agents available')
                
#     # If there are still agents available, assign them to the port with the lowest score
#     if len(agents) > 0:
#         log.info(f'Assigning agents to port with lowest score')
#         for agent in agents:
#             port = sorted_port_scores[0][0]
#             assignments.update({agent: port})
#             print(f'Agent {agent} assigned to port {port}')
            
#     return assignments

# def assign_agents(port_scores, agents):
#     # The leader needs to distribute the agents according to lowest port score preference (i.e. the port with the lowest score gets the most agents)
#     sorted_port_scores = sorted(port_scores.items(), key=lambda x: x[1])
#     for port, score in sorted_port_scores:
#         print(f'Port: {port}, Score: {score}')
        
#     total_port_score = sum(port_scores.values())
        
#     mean_port_score = total_port_score / len(ports)
#     print(f'Mean port score: {mean_port_score}')
    
#     median_port_score = sorted_port_scores[math.floor(len(ports) / 2)][1]
#     print(f'Median port score: {median_port_score}')

#     mean_agents = copy.deepcopy(agents)
#     median_agents = copy.deepcopy(agents)
#     assignment1 = mean_assignment(mean_port_score, sorted_port_scores, mean_agents)
#     assignment2 = median_assignment(median_port_score, sorted_port_scores, median_agents)
    
#     assignments = (assignment1, assignment2)
    
#     return assignments
    
# assignments = assign_agents(port_scores, agents)

# print(f'Port scores: {port_scores}')
# print(f'Mean Assignments: {assignments[0]}')
# print(f'Median Assignments: {assignments[1]}')
