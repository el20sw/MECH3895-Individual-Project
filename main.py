from base_classes.network import Network

# Create a network object
network = Network()

# Add connections to the network
network.add_connection('A', 'B', 1)
network.add_connection('A', 'C', 2)
network.add_connection('B', 'C', 3)
network.add_connection('B', 'D', 4)
network.add_connection('D', 'E', 3)
network.add_connection('D', 'F', 4)
network.add_connection('E', 'C', 1)

# Print the network
network.print_network()

# Draw the network
network.draw_network()
