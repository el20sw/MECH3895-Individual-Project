# Agent class represents an agent (robot) in the simulation moves between nodes at a set speed
class Agent:
    # Constructor given speed (m/s), start location, the network and an id
    def __init__(self, id, speed, start_node, network):
        self.id = id
        self.speed = speed
        self.start_node = start_node
        self.network = network
        self.current_node = start_node
        self.current_path = []
        self.running_time = 0
    
    # Method to get the id of the agent
    def get_id(self):
        return self.id

    # Method to get the possible moves the agent can make given the node it is at
    def get_possible_moves(self, node):
        # Get the adjacency list
        adjacency_list = self.network.get_adjacency_list()
        # Get the possible moves
        possible_moves = adjacency_list[node]
        # Return the possible moves
        return possible_moves

