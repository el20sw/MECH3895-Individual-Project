# Create base_test function
def base_test():
    # Signpost
    print('\nRunning base test...')

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

    # Construction test
    pipeline_test(network)

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

# Pipeline test - test if pipeline network is constructed correctly
def pipeline_test(network):
    # Signpost
    print('\nRunning construction test...')

    # Test nodes in network object
    try:
        assert network.get_node_ids() == {'A', 'B', 'C', 'D', 'E', 'F'}, 'Nodes are not correct'
        network_flag = "Pass"
    except AssertionError:
        network_flag = "Fail"

    print(f"Testing Node construction: {network_flag}")

    # Test connections in network object
    # FIXME: Get this to work, the adjacency list is not equating maybe?
    try:
        assert network.get_adjacency_list() == {
            'A': {'B': (10.0,), 'C': (20.0,)}, 
            'B': {'A': (10.0,), 'C': (30.0,), 'D': (40.0,)}, 
            'C': {'A': (20.0,), 'B': (30.0,), 'E': (10.0,)}, 
            'D': {'B': (40.0,), 'E': (30.0,), 'F': (40.0,)}, 
            'E': {'D': (30.0,), 'C': (10.0,)}, 
            'F': {'D': (40.0,)}
            }, 'Connections are not correct'
        network_flag = "Pass"
    except AssertionError:
        network_flag = "Fail"

    print(f"Testing Pipeline construction: {network_flag}")

# TODO: Test that all relevant data can be gotten - pipe lengths, node ids, etc.