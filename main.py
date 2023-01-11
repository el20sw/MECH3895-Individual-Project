from base_classes.network import Network
from base_classes.agent import Agent

# Create a network object
network = Network()

# Add connections to the network
network.add_connection('A', 'B', 10)
network.add_connection('A', 'C', 20)
network.add_connection('B', 'C', 30)
network.add_connection('B', 'D', 40)
network.add_connection('D', 'E', 30)
network.add_connection('D', 'F', 40)
network.add_connection('E', 'C', 10)

# Create an agent object at node A with speed 1
agent = Agent(1, 1, 'A', network)

# Print the possible moves
agent.print_possible_moves()

# Move the agent to node B
agent.move_to_node('B')

# Print the possible moves
agent.print_possible_moves()

# Move the agent to node C
agent.move_to_node('C')

# Print the possible moves
agent.print_possible_moves()

# Move the agent to node D
agent.move_to_node('D')

# Print the possible moves
agent.print_possible_moves()

# Move the agent to node A
agent.move_to_node('A')

# Print the possible moves
agent.print_possible_moves()

# Draw the network
network.draw_network()
