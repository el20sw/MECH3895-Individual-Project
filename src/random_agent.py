# Import modules
import random
import src.debug.logger as logger

from src.agent import Agent, coroutine
from src.belief import Belief
from src.observation import Observation
from src.transmittable import Transmittable
from src.network import Network

### Random Agent Class ###
class RandomAgent(Agent):
    # constructor for the random agent class
    def __init__(self, environment : Network, id, position, communication_range : int =-1):
        """
        Constructor for the random agent class
        :param environment: Environment in which the agent is operating - the pipe network
        :param id: ID of the agent
        :param position: Position of the agent in the environment
        :param communication_range: Communication range of the agent - defaults to -1 (infinite)
        """

        # create logger
        self.log = logger.get_logger(__name__)

        # set the random seed
        random.seed(0)
        self.log.info(f"Agent {id} is using random seed 0")
        
        # set the agent's id, position and communication range
        self._id = id
        self._position = position
        self._communication_range = communication_range
        self._visited_nodes = []

        # check if the position is in the network environment
        if self._position not in environment.node_names:
            raise ValueError(f'Position {self._position} is not in the network environment')

        # Check if the position is in the adjacency list
        if self._position not in environment.adj_list.keys():
            raise KeyError(f'Position {self._position} is not in adjacency list')

        # Create the agent's belief - takes the environment, the agent's id and the agent's position
        self._belief = Belief(environment, self._id, self._position)

        # initialise if the agent is stepping
        self._stepping = False

    @property
    def id(self):
        """
        Getter for the agent's id
        :return: Agent's id
        """
        return self._id

    @property
    def position(self):
        """
        Getter for the agent's position
        :return: Agent's position
        """
        return self._position

    @property
    def communication_range(self):
        """
        Getter for the agent's communication range
        :return: Agent's communication range
        """
        return self._communication_range

    @property
    def belief(self):
        """
        Getter for the agent's belief
        :return: Agent's belief
        """
        return self._belief
    
    @coroutine
    def step(self, environment, overwatch):
        """
        This is a turn - a step in the simulation for a single agent

        The order of operations is as follows:
        1. Observe
        2. Communicate
        3. Decide
        4. Move

        :return: None
        """
        
        while True:
            stage = yield
            # Step 1: Observe
            if stage == 'observe':
                self.observe(environment)
            # Step 2: Communicate
            elif stage == 'communicate':
                self.communicate(overwatch)
            # Step 3: Decide
            elif stage == 'decide':
                self.action()
            # Step 4: Move
            elif stage == 'move':
                self.move()

    def move(self):
        """
        Method to move the agent in the environment
        :param action: Action to take - the new position of the agent
        :return: None
        """
        
        # update the agent's position
        self._position = self._action
        # log the agent's position
        self.log.info(f"Agent {self._id} is moving to {self._position}")

    def observe(self, environment):
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
        # update the visited nodes
        self._visited_nodes.append(self._position)

        self._observation =  observation

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
            self._tx(self._id, transmittable, agents_in_range, overwatch)
            # request the transmittables from the agents in range - this is handled by the overwatch
            transmittables = self._rx(self._id, overwatch)
            # log the transmittables
            self.log.info(f"Agent {self._id} is receiving {transmittables}")
            # update the agent's belief with the transmittables
            self._belief.update(transmittables)

    def _tx(self, id, transmittable, agents_in_range, overwatch):
        """
        Method to transmit a transmittable to the agents in range
        :param id: Id of the agent
        :param transmittable: Transmittable to transmit
        :param agents_in_range: Agents in range to transmit to
        :param overwatch: Overwatcher
        :return: None
        """

        # call the overwatch receive method
        overwatch.receive(id, transmittable, agents_in_range)

    def _rx(self, id, overwatch):
        """
        Method to receive transmittables from the overwatch
        :param id: Id of the agent
        :param overwatch: Overwatcher
        :return: Transmittables received
        """
            
        # call the overwatch send method
        return overwatch.send(id)

    def action(self):
        """
        Method to get the action of the agent - update the action space
        :return: None
        """

        # Get the action space - this is the list of possible actions (i.e. the nodes adjacent to the agent's current position)
        action_space = self._observation.state['neighbours']
        # log the action space
        self.log.info(f"Agent {self._id} action space: {action_space}")

        # get a random action from the action space
        action = self._random_action(action_space)
        # log the action
        self.log.info(f"Agent {self._id} is taking action {action}")

        self._action = action

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
