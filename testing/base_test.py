# Create base_test function
def base_test():
    # Import the network and agent classes
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

    ### Testing at node A ###
    # Test the agent's current node
    assert agent.get_current_node() == 'A', 'Current node is not correct'
    # Test the agent's possible moves from node A
    assert agent.get_possible_moves('A') == ['B', 'C'], 'Possible moves are not correct'
    # Test the agent's current path
    assert agent.get_current_path() == [], 'Current path is not correct'
    # Test the agent's current running time
    assert agent.get_running_time() == 0, 'Running time is not correct'

    ### Testing at node B ###
    # Move the agent to node B
    agent.move_to_node('B')
    # Test the agent's current node
    assert agent.get_current_node() == 'B', 'Current node is not correct'
    # Test the agent's possible moves from node B
    assert agent.get_possible_moves(agent.current_node) == ['A', 'C', 'D'], 'Possible moves are not correct'
    # Test the agent's current path
    assert agent.get_current_path() == ['A'], 'Current path is not correct'
    # Test the agent's current running time
    assert agent.get_running_time() == 10, 'Running time is not correct'

    ### Testing at node C ###
    # Move the agent to node C
    agent.move_to_node('C')
    # Test the agent's current node
    assert agent.get_current_node() == 'C', 'Current node is not correct'
    # Test the agent's possible moves from node C
    assert agent.get_possible_moves(agent.current_node) == ['A', 'B', 'E'], 'Possible moves are not correct'
    # Test the agent's current path
    assert agent.get_current_path() == ['A', 'B'], 'Current path is not correct'
    # Test the agent's current running time
    assert agent.get_running_time() == 40, 'Running time is not correct'

    ### Testing at node D ###
    # Move the agent to node D
    agent.move_to_node('D')
    # Test the agent's current node - should fail to make the move and so be at C
    assert agent.get_current_node() == 'C', 'Current node is not correct'
    # Test the agent's possible moves from node C
    assert agent.get_possible_moves(agent.current_node) == ['A', 'B', 'E'], 'Possible moves are not correct'
    # Test the agent's current path
    assert agent.get_current_path() == ['A', 'B'], 'Current path is not correct'
    # Test the agent's current running time
    assert agent.get_running_time() == 40, 'Running time is not correct'

    ### Testing at node A ###
    # Move the agent to node A
    agent.move_to_node('A')
    # Test the agent's current node
    assert agent.get_current_node() == 'A', 'Current node is not correct'
    # Test the agent's possible moves from node A
    assert agent.get_possible_moves(agent.current_node) == ['B', 'C'], 'Possible moves are not correct'
    # Test the agent's current path
    assert agent.get_current_path() == ['A', 'B', 'C'], 'Current path is not correct'
    # Test the agent's current running time
    assert agent.get_running_time() == 60, 'Running time is not correct'
