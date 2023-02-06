from abc import ABC, abstractmethod

from src.belief import Belief
from src.observation import Observation

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

    def __init__(self, environment, agent_id, position, communication_range=1) -> None:
        """
        Constructor for the simple agent class
        :param environment: Environment in which the agent is operating - the pipe network
        :param agent_id: ID of the agent
        :param position: Position of the agent in the environment
        :param communication_range: Communication range of the agent
        """

        self._id = agent_id
        self._position = position
        self._previous_position = None
        self._communication_range = communication_range
        self._visited_nodes = []

        # Check if the position is in the network environment and a node
        if self._position not in environment.node_names():
            raise ValueError(f'Position {self._position} is not in the network environment')

        # Check if the position is in the adjacency list
        if self._position not in environment.get_adj_list().keys():
            raise KeyError(f'Position {self._position} is not in adjacency list')

        # Create the agent's belief - takes the environment, the agent's id and the agent's position
        self._belief = Belief(environment, self._id, self._position)

    @abstractmethod
    def step(self) -> None:
        """
        This is a turn
        :return: None
        """

    @abstractmethod
    def move(self) -> None:
        """
        Method to move the agent to the new position in the environment
        :return: None
        """

    @abstractmethod
    def observe(self, environment) -> Observation:
        """
        Method to get the observation of the agent - update the observation space
        :param environment: Environment in which the agent is observing - the pipe network
        :update: Update the visited nodes
        :return: Observation of the agent
        """

    @abstractmethod
    def communicate(self, overwatch):
        """
        Method to communicate with other agents in the environment - send and receive transmissions
        :param environment: Environment in which the agent is communicating - the pipe network
        :return: None
        """

    @abstractmethod
    def comms_part1(self, overwatch):
        """
        Method to send a communication to other agents in the environment
        :param overwatch: overwatcher facilitating communication
        :return: None
        """

    @abstractmethod
    def comms_part2(self, overwatch):
        """
        Method to recieve communication from other agents in the environment
        :param overwatch: overwatcher facilitating communication
        :return: None
        """

    @abstractmethod
    def _tx(self, agent_id, transmittable, agents_in_range, overwatch):
        """
        Method to transmit a transmittable to the agents in range
        :param id: Id of the agent
        :param transmittable: Transmittable to transmit
        :param agents_in_range: Agents in range to transmit to
        :param overwatch: Overwatcher
        :return: None
        """

    @abstractmethod
    def _rx(self, agent_id, overwatch):
        """
        Method to receive transmittables from the agents in range
        :param id: Id of the agent
        :param overwatch: Overwatcher
        :return: Transmittables received
        """

    @abstractmethod
    def action(self):
        """
        Method to get the action of the agent - update the action space
        :return: Action of the agent
        """

    @property
    def agent_id(self) -> int:
        """
        Method to get the ID of the agent
        :return: ID of the agent
        """
        return self._id

    @property
    def position(self):
        """
        Method to get the position of the agent
        :return: Position of the agent
        """
        return self._position

    @property
    def previous_position(self):
        """
        Method to get the previous position of the agent
        :return: Previous position of the agent
        """
        return self._previous_position

    @property
    def communication_range(self) -> int:
        """
        Method to get the communication range of the agent
        :return: Communication range of the agent
        """
        return self._communication_range

    @property
    def belief(self) -> Belief:
        """
        Method to get the belief of the agent
        :return: Belief of the agent
        """
        return self._belief

    @property
    def visited_nodes(self) -> list:
        """
        Method to get the visited nodes of the agent
        :return: Visited nodes of the agent
        """
        return self._visited_nodes

    def __str__(self) -> str:
        return f'Agent {self._id}'

    def __repr__(self) -> str:
        return f'Agent {self._id}'

# Coroutine decorator
def coroutine(func):
    """
    Coroutine decorator
    ----------
    Decorator to start a coroutine
    """
    def start(*args,**kwargs):
        routine = func(*args,**kwargs)
        routine.next()
        return routine
    return start
