### Import modules
import src.debug.logger as logger
from abc import ABC, abstractmethod

### Base Agent Class ###
class Agent(ABC):
    """
    Base Agent Class
    ----------
    Abstract class for agents - all agents should inherit from this class

    :param environment: Environment in which the agent is operating - the pipe network
    :param agent_id: ID of the agent
    :param position: Position of the agent in the environment (starting position)
    :param communication_range: Communication range of the agent
    """

    def __init__(self, environment, id, position, communication_range=1) -> None:
        """
        Constructor for the simple agent class
        :param environment: Environment in which the agent is operating - the pipe network
        :param id: ID of the agent
        :param position: Position of the agent in the environment
        :param communication_range: Communication range of the agent
        """

        self._id = id
        self._position = position
        self._communication_range = communication_range

        self._visited_nodes = []

        # Check if the position is in the network environment and a node
        if self._position not in environment.node_names():
            raise ValueError(f'Position {self._position} is not in the network environment')

        # Check if the position is in the adjacency list
        if self._position not in environment.get_adj_list().keys():
            raise KeyError(f'Position {self._position} is not in adjacency list')

    @abstractmethod
    def move(self, environment, action) -> None:
        """
        Method to move the agent in the environment
        :param environment: Environment in which the agent is moving - the pipe network
        :param action: Action to take - the new position of the agent
        :return: None
        """
        pass

    @abstractmethod
    def observe(self, environment) -> dict:
        """
        Method to get the observation of the agent - update the observation space
        :param environment: Environment in which the agent is observing - the pipe network
        :param other_agents: Other agents in the environment
        :update: Update the visited nodes
        :return: Observation of the agent
        """
        pass

    @abstractmethod
    def communicate(self, environment) -> None:
        """
        Method to communicate with other agents in the environment - send and receive transmissions
        :param environment: Environment in which the agent is communicating - the pipe network
        :return: None
        """
        pass

    @abstractmethod
    def action(self, observation) -> str:
        """
        Method to get the action of the agent - update the action space
        :param observation: Observation of the agent
        :return: Action of the agent
        """
        pass

    @property
    def id(self) -> int:
        """
        Method to get the ID of the agent
        :return: ID of the agent
        """
        return self._id

    @property
    def position(self) -> str:
        """
        Method to get the position of the agent
        :return: Position of the agent
        """
        return self._position

    @property
    def communication_range(self) -> int:
        """
        Method to get the communication range of the agent
        :return: Communication range of the agent
        """
        return self._communication_range

    @property
    def visited_nodes(self) -> list:
        """
        Method to get the visited nodes of the agent
        :return: Visited nodes of the agent
        """
        return self._visited_nodes

