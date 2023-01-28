### Logger Setup ###
import debug.logger as logger
log = logger.setup_logger(file_name='logs/greedy_agent_test.log')

### Module Imports ###
from src.simulation import Simulation
from src.pipe_network import PipeNetwork
from src.greedy_agent import GreedyAgent

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
agent = GreedyAgent(env, 0, '11')

# Add agents to simulation
log.debug('Adding agents to simulation')
sim.add_agent(agent)

# Log the agents
log.info(f'Agents: {sim.agents}')

# Run simulation
log.debug('Running simulation')
sim.run(max_turns=100)

# Get results
results = sim.get_results()

# Write results to file
sim.write_results_to_file()

# Get the possible junctions in ordered form
junctions = env.get_junction_names()
junctions = sorted(junctions)
log.info(f'All Junctions: {junctions}')
# Get the visited junctions
visited_junctions = results['visited_junctions']
visited_junctions = sorted(visited_junctions)
log.info(f'Visited Junctions: {visited_junctions}')

# Render the network
env.render_network(node_labels=True, link_labels=True)
