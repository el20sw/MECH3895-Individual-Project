### Imports ###
import random


# Agent class represents an agent (robot) in the simulation moves between nodes at a set speed
class Agent:
    # Constructor given speed (m/s), start location, the network and an id
    def __init__(self, id, speed: float, start_node, network):
        self.id = id
        self.speed = speed
        self.start_node = start_node
        self.network = network
        self.current_node = start_node
        self.current_path = []
        self.running_time = 0
        self.visited_nodes = {}

    ### Getters and Setters ###
    # Method to get the id of the agent
    def get_id(self):
        return self.id

    # Method to set the id of the agent
    def set_id(self, id):
        self.id = id

    # Method to get the speed of the agent
    def get_speed(self):
        return self.speed

    # Method to set the speed of the agent
    def set_speed(self, speed):
        self.speed = speed

    # Method to get the start node of the agent
    def get_start_node(self):
        return self.start_node

    # Method to set the start node of the agent
    def set_start_node(self, start_node):
        self.start_node = start_node

    # Method to get the current node of the agent
    def get_current_node(self):
        return self.current_node

    # Method to set the current node of the agent
    def set_current_node(self, current_node):
        self.current_node = current_node

    # Method to get the current path
    def get_current_path(self):
        return self.current_path

    # Method to set the current path
    def set_current_path(self, current_path):
        self.current_path = current_path

    # Method to get the running time of the agent
    def get_running_time(self):
        return self.running_time

    # Method to set the running time of the agent
    def set_running_time(self, running_time):
        self.running_time = running_time

    # Method to get the visited nodes
    def get_visited_nodes(self):
        return self.visited_nodes

    # Method to set the visited nodes
    def set_visited_nodes(self, visited_nodes):
        self.visited_nodes = visited_nodes

    ### Getting Possible Moves ###
    # Method to get the possible moves the agent can make given the node it is at
    def get_possible_moves(self, node):
        # Get the adjacency list
        adjacency_list = self.network.get_adjacency_list()
        # Get the possible moves
        possible_moves = list(adjacency_list[node].keys())
        return possible_moves


    # Method to print the current possible moves
    def print_possible_moves(self):
        print(f'Agent {self.id} at {self.current_node} can move to: ', self.get_possible_moves(self.current_node))

    ### Moving the Agent ###
    # Method to move the agent to a given node
    def move_to_node(self, node=None):
        # check if the target node is in the possible moves
        if node not in self.get_possible_moves(self.current_node):
            return False
        # get the pipe length of the desired move
        pipe_length = self.network.get_pipe_length(self.current_node, node)
        # add the agents current node to the path
        self.update_path(self.current_node)
        # set the agents current node to the target node
        self.set_current_node(node)
        # calculate the time to move to the node
        time_to_move = pipe_length / self.speed
        # update the running time
        self.update_time(time_to_move)

    # Debug method to move the agent to a given node
    def debug_move_to_node(self, node=None):
        # check if the target node is in the possible moves
        if node not in self.get_possible_moves(self.current_node):
            print(f"{node} is not a possible move from node {self.current_node}")
            return False
        # get the pipe length of the desired move
        pipe_length = self.network.get_pipe_length(self.current_node, node)
        # add the agents current node to the path
        self.update_path(self.current_node)
        # set the agents current node to the target node
        self.set_current_node(node)
        # calculate the time to move to the node
        time_to_move = pipe_length / self.speed
        # update the running time
        self.update_time(time_to_move)
        ### Debugging ###
        # print the pipe length
        print(f"Pipe length: {pipe_length}")
        # print the agents current node
        print(f"Agent {self.id} is now at node {self.current_node}")
        # print the agents current path
        print(f"Agent {self.id} current path: {self.current_path}")
        # print the agents running time
        print(f"Agent {self.id} running time: {self.running_time}")

    # Method to move the agent to a random node
    def move_to_random_node(self):
        # get the possible moves
        possible_moves = self.get_possible_moves(self.current_node)
        # get a random node
        random_node = random.choice(possible_moves)
        # move to the random node
        self.move_to_node(random_node)

    # Method to update the path
    def update_path(self, node):
        # get the agent's current path
        current_path = self.get_current_path()
        # add the current node to the path
        current_path.append(node)

    # Method to update the time
    def update_time(self, time):
        # get the current time
        current_time = self.get_running_time()
        # update the time
        self.set_running_time(current_time + time)

    # Method to get metadata
    def get_metadata(self):
        return {'id': self.id, 'speed': self.speed, 'start_node': self.start_node, 'current_node': self.current_node, 'current_path': self.current_path, 'running_time': self.running_time}
