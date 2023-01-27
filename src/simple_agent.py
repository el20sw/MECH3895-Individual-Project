# Simple Agent Class
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

    def move(self, action, environment):
        """
        Method to move the agent in the environment
        :param action: Action to take - the new position of the agent
        :param environment: Environment in which the agent is moving - the pipe network
        :return: None
        """
        # Update the agent's position
        self.position = action
        # Add the new position to the list of visited nodes
        self.visited_nodes.append(action)

    def communicate(self, environment):
        """
        Method to communicate with other agents in the environment
        :param environment: Environment in which the agent is communicating - the pipe network
        :return: None
        """
        pass

    def get_observation(self, environment, other_agents):
        """
        Method to get the observation of the agent
        :param environment: Environment in which the agent is observing - the pipe network
        :param other_agents: Other agents in the environment
        :return: Observation of the agent
        """
        observation = {
            'position': self.position,
            'visited_nodes': self.visited_nodes,
            'pipe_network_state': environment.get_state(self.position)
        }
