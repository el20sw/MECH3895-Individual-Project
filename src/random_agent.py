# Import modules
import random
import src.debug.logger as logger

from src.agent import Agent
from src.belief import Belief
from src.observation import Observation
from src.transmittable import Transmittable

### Random Agent Class ###
class RandomAgent(Agent):
    # constructor for the random agent class
    def __init__(self, environment, id, position, communication_range=-1):
        """
        Constructor for the random agent class
        :param environment: Environment in which the agent is operating - the pipe network
        :param id: ID of the agent
        :param position: Position of the agent in the environment
        :param communication_range: Communication range of the agent - defaults to -1 (infinite)
        """

        # create logger
        self.log = logger.setup_logger(file_name='logs/random_agent.log')

        # set the random seed
        random.seed(0)
        self.log.info(f"Agent {id} is using random seed 0")
        
        # set the agent's id, position and communication range
        self._id = id
        self._position = position
        self._communication_range = communication_range

        # Check if the position is in the network environment and a node
        if self._position not in environment.node_names():
            raise ValueError(f'Position {self._position} is not in the network environment')

        # Check if the position is in the adjacency list
        if self._position not in environment.get_adj_list().keys():
            raise KeyError(f'Position {self._position} is not in adjacency list')

        # Create the agent's belief - takes the environment, the agent's id and the agent's position
        self._belief = Belief(environment, self._id, self._position)

    def move(self, environment, action):
        """
        Method to move the agent in the environment
        :param environment: Environment in which the agent is moving - the pipe network
        :param action: Action to take - the new position of the agent
        :return: None
        """
        
        # update the agent's position
        self._position = action
        # log the agent's position
        self.log.info(f"Agent {self._id} is moving to {self._position}")

    def observe(self, environment) -> Observation:
        """
        Method to observe the environment
        :param environment: Environment in which the agent is observing - the pipe network
        :return: Observation of the agent
        """
        
        # create an observation object
        observation = Observation(environment, self._position)
        # log the observation
        self.log.info(f"Agent {self._id} is observing {observation}")
        # update the belief of the agent with the observation
        self._belief.update(observation)

        return observation

    def communicate(self, overwatch):
        """
        Method to communicate with other agents in the environment
        :param environment: Environment in which the agent is communicating - the pipe network
        :return: None
        """
        
        # query the overwatch for the agents in the agent's communication range
        agents_in_range = overwatch.get_agents_in_range(self._position, self._communication_range)
        # log the agents in range
        self.log.info(f"Agent {self._id} is communicating with {agents_in_range}")

        # if there are agents in range
        if agents_in_range:
            # create transmittable object with the agent's belief
            transmittable = Transmittable(self._belief)
            # log the transmittable
            self.log.info(f"Agent {self._id} is transmitting {transmittable}")
            # send the transmittable to the agents in range - this is handled by the overwatch
            overwatch.send_transmittable(self._id, transmittable, agents_in_range)

    def action(self, observation):
        """
        Method to get the action of the agent - update the action space
        :return: None
        """

        # Get the action space - this is the list of possible actions (i.e. the nodes adjacent to the agent's current position)
        action_space = observation.state['neighbours']
        # log the action space
        self.log.info(f"Agent {self._id} action space: {action_space}")

        # get a random action from the action space
        action = self._random_action(action_space)
        # log the action
        self.log.info(f"Agent {self._id} is taking action {action}")

        return action

    def _random_action(self, action_space):
        """
        Method to get a random action from the action space
        :param action_space: Action space - list of possible actions
        :return: Random action
        """
          
        # get a random action from the action space
        action = random.choice(action_space)
        # log the action
        self.log.info(f"Agent {self._id} is taking action {action}")

        return action
