from src.overwatch import OverWatch
from src.pipe_network import PipeNetwork
from src.random_agent import RandomAgent

# Initialise an environment
env = PipeNetwork('networks/Net1.inp')
# Initialise an agent
agent = RandomAgent(env, 0, '11')
# Initialise an agent
agent2 = RandomAgent(env, 1, '22')

# Initialise the overwatch
ow = OverWatch(env, [agent, agent2])

# Get the agent positions
print(ow.get_agent_positions())

# Get the visited nodes
print(ow.get_visited_junctions())

# Move the agents to new positions
def move_agent(agent):
    obv = agent.get_observation(env)
    act = agent.get_action(obv)
    agent.move(env, act)

# Move the agents
move_agent(agent)
move_agent(agent2)

# Get the agent positions
print(ow.get_agent_positions())

# Get the visited nodes
print(ow.get_visited_junctions())

# Move the agents to new positions
move_agent(agent)
move_agent(agent2)

# Get the agent positions
print(ow.get_agent_positions())

# Get the visited nodes
print(ow.get_visited_junctions())

# Print all the nodes
print(ow.all_junctions)
