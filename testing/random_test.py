# Create random test function
def random_test():
    # Signpost
    print('\nRunning random test...\n')

    # Import the network and agent classes
    from base_classes.network import Network
    from base_classes.agent import Agent
    import random

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

    # Agent moves to random nodes until all nodes are visited
    while len(set(agent.current_path)) < len(network.nodes):
        # Agent moves to random node
        agent.move_to_random_node()
        # Test the agent's possible moves from current node
        assert agent.get_possible_moves(agent.current_node) == network.get_possible_moves(agent.current_node), 'Possible moves are not correct'

    # Test that the agent has visited all nodes
    assert len(set(agent.current_path)) == len(network.nodes), 'Agent has not visited all nodes'

    