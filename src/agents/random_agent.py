# Import modules
from typing import List
import src.debug.logger as logger

from src.agents.agent import Agent, coroutine
from src.belief import Belief
from src.observation import Observation
from src.transmittable import Transmittable
from src.network import Network
from src.overwatch import Overwatch

import random
import asyncio

### Random Agent Class ###
class RandomAgent(Agent):
    # constructor for the random agent class
    def __init__(self, environment : Network, id, position, communication_range : int =-1, random_seed : int = 0):
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
        random.seed(random_seed)
        self.log.info(f"Agent {id} is using random seed {random_seed}")
        
        # set the agent's id, position and communication range
        self._id = id
        self._position = position
        self._previous_position = None
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

    @property
    def agent_id(self):
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
    def previous_position(self):
        """
        Getter for the agent's previous position
        :return: Agent's previous position
        """
        return self._previous_position

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

    @property
    def observation(self):
        """
        Getter for the agent's observation
        :return: Agent's observation
        """
        return self._observation
    
    async def step(self, environment, overwatch):
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
        # update the previous position
        self._previous_position = self._position        
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
        
    # NOTE: This method does not work
    def communicate(self, overwatch):
        """
        Method to communicate with other agents in the environment
        :param environment: Environment in which the agent is communicating - the pipe network
        :return: None
        """
        
        # query the overwatch for the agents in the agent's communication range
        agents_in_range = overwatch.get_agents_in_range(self._position, self._communication_range)
        # remove the agent's own id from the list of agents in range
        agents_in_range = [agent for agent in agents_in_range if agent.agent_id != self._id]
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
            self._belief.update()

    def comms_part1(self, overwatch):
        """
        Method to send a communication to other agents in the environment
        :param overwatch: overwatcher facilitating communication
        :return: None
        """

        # query the overwatch for the agents in the agent's communication range
        agents_in_range = overwatch.get_agents_in_range(self._position, self._communication_range)
        # remove the agent's own id from the list of agents in range
        agents_in_range = [agent for agent in agents_in_range if agent.agent_id != self._id]
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

    def comms_part2(self, overwatch):
        """
        Method to recieve communication from other agents in the environment
        :param overwatch: overwatcher facilitating communication
        :return: None
        """

        # request the transmittables from the agents in range - this is handled by the overwatch
        transmittables = self._rx(self._id, overwatch)
        # log the transmittables
        self.log.info(f"Agent {self._id} is receiving {transmittables}")
        # update the agent's belief with the transmittables
        self._belief.update(*transmittables)

    def send_communication(self, overwatch):
        """
        Method to send communication to the overwatch
        :param overwatch: Overwatcher
        :return: None
        """

        # query the overwatch for the agents in the agent's communication range
        self._agents_in_range = overwatch.get_agents_in_range(self._position, self._communication_range)
        # remove the agent's own id from the list of agents in range
        self._agents_in_range = [agent for agent in self._agents_in_range if agent.agent_id != self._id]
        # log the agents in range
        self.log.info(f"Agent {self._id} is communicating with {self._agents_in_range}")

        # if there are agents in range
        if self._agents_in_range:
            # create transmittable object with the agent's belief
            self._transmittable = Transmittable(self._belief)
            # log the transmittable
            self.log.info(f"Agent {self._id} is transmitting {self._transmittable}")
            # send the transmittable to the agents in range - this is handled by the overwatch
            self._tx(self._id, self._transmittable, self._agents_in_range, overwatch)

    def receive_communication(self, overwatch) -> List[Transmittable]:
        """
        Method to receive communication from the overwatch
        :param overwatch: Overwatcher
        :return: Transmittables received
        """

        # request the transmittables from the agents in range - this is handled by the overwatch
        self._transmittables = self._rx(self._id, overwatch)
        # log the transmittables
        self.log.info(f"Agent {self._id} is receiving {self._transmittables}")

        return self._transmittables

    def update_belief(self, *transmittables: Transmittable):
        """
        Method to update the agent's belief with the transmittables
        :param transmittables: Transmittables to update the belief with
        :return: None
        """

        # update the agent's belief with the transmittables
        self._belief.update(*transmittables)

    def _tx(self, id, transmittable, agents_in_range, overwatch: Overwatch):
        """
        Method to transmit a transmittable to the agents in range
        :param id: Id of the agent
        :param transmittable: Transmittable to transmit
        :param agents_in_range: Agents in range to transmit to
        :param overwatch: Overwatcher
        :return: None
        """

        # call the overwatch receive method
        overwatch.upload(id, transmittable, agents_in_range)

    def _rx(self, agent_id, overwatch: Overwatch) -> List[Transmittable]:
        """
        Method to receive transmittables from the overwatch
        :param id: Id of the agent
        :param overwatch: Overwatcher
        :return: Transmittables received
        """
            
        # call the overwatch send method
        return overwatch.download(agent_id)

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