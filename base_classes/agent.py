### Import modules
import numpy as np

### Simple Agent Class ###
class SimpleAgent:
    # Constructor for the simple agent class
    def __init__(self, environment, agent_id, position, communication_range=100):
        """
        Constructor for the simple agent class
        :param environment: Environment in which the agent is operating - the pipe network
        :param agent_id: ID of the agent
        :param position: Position of the agent in the environment
        :param communication_range: Communication range of the agent
        """

        self.agent_id = agent_id
        self.position = position
        self.communication_range = communication_range
        self.visited_nodes = []

        # Check if the position is in the network environment
        if self.position not in environment.get_node_names():
            raise ValueError(f'Position {self.position} is not in the network environment')

        # Check if the position is in the adjacency list
        if self.position not in environment.get_adj_list().keys():
            raise KeyError(f'Position {self.position} is not in adjacency list')

    def move(self, environment, action):
        """
        Method to move the agent in the environment
        :param action: Action to take - the new position of the agent
        :param environment: Environment in which the agent is moving - the pipe network
        :return: None
        """

        # FIXME: Debug Print Statement
        print(f"Agent {self.agent_id} is moving")

        # Update the agent's position
        self.position = action

    def communicate(self, environment):
        """
        Method to communicate with other agents in the environment
        :param environment: Environment in which the agent is communicating - the pipe network
        :return: None
        """
        pass

    def get_observation(self, environment, other_agents=None):
        """
        Method to get the observation of the agent - update the observation space
        :param environment: Environment in which the agent is observing - the pipe network
        :param other_agents: Other agents in the environment
        :update: Update the visited nodes
        :return: Observation of the agent
        """

        # FIXME: Debug Print Statement
        print(f"Agent {self.agent_id} is observing")

        observation = {
            'position': self.position,
            'visited_nodes': self.visited_nodes,
            'pipe_network_state': environment.get_state(self.position),
            'other_agents': other_agents
        }
        self.visited_nodes.append(self.position)

        return observation

    def get_action(self, observation):
        """
        Method to get the action of the agent - update the action space
        :param observation: Observation of the agent
        :return: Action of the agent
        """

        # FIXME: Debug Print Statement
        print(f"Agent {self.agent_id} is getting an action")

        # Get the adjacent nodes
        adjacent_nodes = observation['pipe_network_state']

        # Get the unvisited adjacent nodes
        unvisited_adjacent_nodes = [node for node in adjacent_nodes if node not in observation['visited_nodes']]

        # Get the action space
        action = {
            'adjacent_nodes': adjacent_nodes,
            'unvisited_adjacent_nodes': unvisited_adjacent_nodes
        }

        return action

    def get_visited_nodes(self):
        return self.visited_nodes()
