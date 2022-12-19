from base_classes.network import Network

# Create a network object
network = Network()
# Add nodes to the network
network.add_node('A')
network.add_node('B')
network.add_node('C')
network.add_node('D')
network.add_node('E')

# Add pipes to the network
network.add_pipe(1, 'A', 'B')
network.add_pipe(2, 'A', 'C')
network.add_pipe(3, 'B', 'C')
network.add_pipe(4, 'B', 'D')
network.add_pipe(5, 'C', 'D')
network.add_pipe(6, 'C', 'E')
network.add_pipe(7, 'D', 'E')

# Print the network
network.print_network()

# Draw the network
network.draw_network()
