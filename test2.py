from src.simulation import Simulation
from src.pipe_network import PipeNetwork
from src.simple_agent import SimpleAgent

# Create PipeNetwork environment
env = PipeNetwork('networks/Net1.inp')

# Get the possible starting nodes
nodes = env.get_node_names()


# Create simulation
sim = Simulation(env)

# Create agent
agent = SimpleAgent(env, 0, nodes[1])

# Add agent to simulation
sim.add_agent(agent)

# Run simulation
sim.run()

# Get results
results = sim.get_results()

# Write results to file
sim.write_results_to_file()

# Render the network
env.render_network(node_labels=True, link_labels=True)
