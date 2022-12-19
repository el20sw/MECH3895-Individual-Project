from base_classes.network import Network

# # Create a network object
# network = Network()
# # Add nodes to the network
# network.add_node('A')
# network.add_node('B')
# network.add_node('C')
# network.add_node('D')
# network.add_node('E')
# network.add_node('F')

# # Add pipes to the network
# network.add_pipe(1, 'A', 'B')
# network.add_pipe(2, 'A', 'C')
# network.add_pipe(3, 'B', 'C')
# network.add_pipe(4, 'B', 'D')
# network.add_pipe(3, 'D', 'E')
# network.add_pipe(4, 'D', 'F')
# network.add_pipe(1, 'E', 'C')

# # Print the network
# network.print_network()

# # Draw the network
# network.draw_network()

# Create a network object
network2 = Network()

# Add connections to the network
network2.add_connection('A', 'B', 1)
network2.add_connection('A', 'C', 2)
network2.add_connection('B', 'C', 3)
network2.add_connection('B', 'D', 4)
network2.add_connection('D', 'E', 3)
network2.add_connection('D', 'F', 4)
network2.add_connection('E', 'C', 1)

# Print the network
network2.print_network()

# Draw the network
network2.draw_network()
