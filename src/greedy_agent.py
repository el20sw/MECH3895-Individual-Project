# Import logger
import debug.logger as logger

### Import modules
from src.agent import Agent

### Greedy Agent Class ###
class GreedyAgent(Agent):
    # Constructor for the greedy agent class
    def __init__(self, environment, agent_id, position, communication_range=100):
        """
        Constructor for the greedy agent class
        :param environment: Environment in which the agent is operating - the pipe network
        :param agent_id: ID of the agent
        :param position: Position of the agent in the environment
        :param communication_range: Communication range of the agent
        """

        # Create logger
        self.log = logger.setup_logger(file_name='logs/greedy_agent.log')

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

        # Update the agent's position
        self.position = action
        # Log the agent's position
        self.log.info(f"Agent {self.agent_id} is moving to {self.position}")

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
        :return: None
        """

        # Get the observation space
        observation = {
            'position': self.position,
            'visited_nodes': self.visited_nodes,
            'pipe_network_state': environment.get_state(self.position),
            'other_agents': other_agents
        }

        # Log the agent's observation
        self.log.info(f"Agent {self.agent_id} is observing {observation['pipe_network_state']}")

        return observation

    def get_action(self, observation):
        """
        Method to get the action of the agent - update the action space
        :param observation: Observation of the agent
        :return: Action of the agent
        """

        # Get the action space
        adjacent_nodes = observation['pipe_network_state']

        # Get the unvisited adjacent nodes
        unvisited_adjacent_nodes = [node for node in adjacent_nodes if node not in observation['visited_nodes']]

        # Get the action space
        action_space = {
            'adjacent_nodes': adjacent_nodes,
            'unvisited_adjacent_nodes': unvisited_adjacent_nodes
        }

        action = self.greedy_action(action_space)

        # Log the agent's action
        self.log.info(f"Agent {self.agent_id} is taking action {action}")

        return action

    def get_visited_nodes(self):
        """
        Method to get the visited nodes
        :return: Visited nodes
        """
        return self.visited_nodes

    def greedy_action(self, action_space):
        """
        Method to get the greedy action of the agent
        :param action_space: Action space of the agent
        :return: Greedy action of the agent
        """
        # Check if there are unvisited adjacent nodes
        if len(action_space['unvisited_adjacent_nodes']) > 0:
            # Logging message
            self.log.info(f"Agent {self.agent_id} is taking a greedy action")
            # Get the greedy action - the nearest unvisited adjacent node
            action = action_space['unvisited_adjacent_nodes'][0]

        else:
            # Logging message
            self.log.info(f"Agent {self.agent_id} is taking a random action")
            # Get the random action - the nearest adjacent node
            action = action_space['adjacent_nodes'][0]

        return action