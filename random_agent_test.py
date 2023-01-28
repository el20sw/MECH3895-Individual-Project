### Logger Setup ###
import debug.logger as logger
log = logger.setup_logger(file_name='logs/random_agent_test.log')

### Module Imports ###
from src.simulation import Simulation
from src.pipe_network import PipeNetwork
from src.random_agent import RandomAgent

# Create PipeNetwork environment
log.debug('Creating PipeNetwork environment')
env = PipeNetwork('networks/Net1.inp')

# Get the possible starting nodes
nodes = env.get_node_names()

# Create simulation
log.debug('Creating simulation')
sim = Simulation(env)

# Create agent
log.debug('Creating agent')
agent = RandomAgent(env, 0, '11')
# Create agent
log.debug('Creating agent')
agent2 = RandomAgent(env, 1, '22')

# Add agents to simulation
log.debug('Adding agents to simulation')
sim.add_agent(agent)
sim.add_agent(agent2)

# Print agents
print(sim.agents)

# Run simulation
log.debug('Running simulation')
sim.run(max_turns=1000)

# Get results
results = sim.get_results()

# Write results to file
sim.write_results_to_file()

# Render the network
env.render_network(node_labels=True, link_labels=True)
