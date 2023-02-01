from src.network import Network
from src.observation import Observation
from src.greedy_agent import GreedyAgent

from copy import deepcopy

# create a network
network = Network('networks/Net1.inp')
# create an agent
agent = GreedyAgent(network, 'A', '11')
# get the agent's belief of the links
a = deepcopy(agent._belief.links)
# create an observation
agent.observe(network)
# get the agent's belief of the links
b = deepcopy(agent._belief.links)
# move agent to a new position
agent._position = '12'
# update the observation
agent.observe(network)
# get the agent's belief of the links
c = deepcopy(agent._belief.links)
# move agent to a new position
agent._position = '13'
# update the observation
agent.observe(network)
# get the agent's belief of the links
d = deepcopy(agent._belief.links)
# move agent to a new position
agent._position = '23'
# update the observation
agent.observe(network)
# get the agent's belief of the links
e = deepcopy(agent._belief.links)
# move agent to a new position
agent._position = '22'
# update the observation
agent.observe(network)
# get the agent's belief of the links
f = deepcopy(agent._belief.links)
# move agent to a new position
agent._position = '12'
# update the observation
agent.observe(network)
# move agent to a new position
agent._position = '11'
# update the observation
agent.observe(network)
# move agent to a new position
agent._position = '21'
# update the observation
agent.observe(network)
# move agent to a new position
agent._position = '31'
# update the observation
agent.observe(network)
# move agent to a new position
agent._position = '32'
# update the observation
agent.observe(network)
# move agent to a new position
agent._position = '22'
# update the observation
agent.observe(network)
# move agent to a new position
agent._position = '32'
# update the observation
agent.observe(network)

print(agent.belief.links)

# generate a link between node 10 and 11 with a length of 10
agent._belief._links.append(('10', '11', {'link_name': 'xyz', 'link_length': 10}))

print(agent.belief.links)

# build adjacency list of agent's belief of the links
adj_list = agent._build_agent_adjacency_list()

print(adj_list)

# test djikstra's algorithm
deg_sep, previous = agent._dijkstra(agent.position, adj_list)

print(deg_sep)
print(previous)

nearest_unvisited_node = agent._get_nearest_unvisited_node(adj_list, deg_sep)

print(nearest_unvisited_node)

actionA = agent._get_action_closer_to_node(
    agent._observation.state['neighbours'], 
    nearest_unvisited_node,
    previous
    )

# move the agent
agent._position = actionA
# update the observation
agent.observe(network)

actionB = agent._get_action_closer_to_node(
    agent._observation.state['neighbours'],
    nearest_unvisited_node,
    previous
    )

# move the agent
agent._position = actionB
# update the observation
agent.observe(network)

actionC = agent._get_action_closer_to_node(
    agent._observation.state['neighbours'],
    nearest_unvisited_node,
    previous
    )

# move the agent
agent._position = actionC
# update the observation
agent.observe(network)

actionD = agent._get_action_closer_to_node(
    agent._observation.state['neighbours'],
    nearest_unvisited_node,
    previous
    )

# move the agent
agent._position = actionD
# update the observation
agent.observe(network)

actionE = agent._get_action_closer_to_node(
    agent._observation.state['neighbours'],
    nearest_unvisited_node,
    previous
    )

# move the agent
agent._position = actionE
# update the observation
agent.observe(network)

print(actionA)
print(actionB)
print(actionC)
print(actionD)
print(actionE)

# plot the network
network.plot_network(show=True, node_labels=True, link_labels=True)