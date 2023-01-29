# Import modules
import debug.logger as logger

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
        - `agents`: the beliefs of the other agents in the environment that are in communication range of the agent
            - the `agents` send copies of their belief states to the agent which the agent can use to update its belief state
    """

    def __init__(self, position, environment, tx=None):
        """
        Constructor for the agent observation class
        :param position: Position of the agent in the environment
        :param environment: Environment in which the agent is operating - the pipe network
        :param tx: Belief states of other agents in communication range
        """
        # Initialise the logger
        self.log = logger.get_logger(__name__)

        # Initialise the observation
        self._position = position                               # agent's current position
        self._state = environment.get_state(self._position)     # state of the environment at the agent's current position
        self._agents = tx                                       # beliefs of other agents in communication range
        
        # Log the observation
        self.log.debug(f'Observation: {self}')
        self.log.info(f'Position: {self._position}')
        self.log.info(f'State: {self._state}')
        self.log.info(f'Agents: {self._agents}')

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

    @property
    def agents(self):
        """
        Agents getter
        :return: Agents
        """
        return self._agents

    # Class method to make observation
    @classmethod
    def observe(cls, position, environment, tx=None):
        """
        Class method to make observation
        :param position: Position of the agent in the environment
        :param environment: Environment in which the agent is operating - the pipe network
        :param tx: Belief states of other agents in communication range
        :return: Observation
        """
        return cls(position, environment, tx)