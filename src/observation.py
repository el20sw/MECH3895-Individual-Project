# Import modules
import src.debug.logger as logger

from src.network import Network

### Agent Observation Class ###
class Observation:
    """
    Agent Observation Class
    ----------
    Class to create an observation for an agent in the environment
    This class is used to create the agent's observation space
    - Observations are instantaneous - they contain the information only accessable to the agent at the current time step
    - Observations contain the information:
        - `position`: the agent's current position in the environment
        - `state`: the state of the environment at the agent's current position
            - the `state` includes the nodes adjacent to the agent's current position
    """

    def __init__(self, environment: Network, position):
        """
        Constructor for the agent observation class
        :param environment: Environment in which the agent is operating - the pipe network
        :param position: Position of the agent in the environment
        """
        # Initialise the logger
        self.log = logger.get_logger(__name__)

        # Initialise the observation
        self._position = position                               # agent's current position
        self._state = environment.get_state(self._position)     # state of the environment at the agent's current position
        
        # Log the observation
        self.log.debug(f'Observation: {self}')
        self.log.debug(f'Position: {self._position}')
        self.log.debug(f'State: {self._state}')

    @property
    def position(self):
        """
        Position getter
        :return: Position
        """
        return self._position

    @property
    def state(self):
        """
        State getter
        :return: State
        """
        return self._state


    # Class method to make observation
    @classmethod
    def observe(cls, position, environment):
        """
        Class method to make observation
        :param position: Position of the agent in the environment
        :param environment: Environment in which the agent is operating - the pipe network
        :return: Observation
        """
        return cls(position, environment)