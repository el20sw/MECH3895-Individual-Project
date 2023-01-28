# Import logger
import debug.logger as logger

### Import modules
from src.agent import Agent
import copy

### Greedy Agent Class ###
class GreedyAgent(Agent):
    """
    # TODO: Add/Finish documentation

    Greedy Agent Class
    ------------------
    This class implements a greedy agent that moves to the nearest unexplored junction

    ### Parameters
    - environment: Environment in which the agent is operating - the pipe network
    - agent_id: ID of the agent
    - position: Starting position of the agent in the environment
    - communication_range: Communication range of the agent (given as number of junctions)

    ### Methods
    - move: Move the agent to the nearest unexplored junction
    - communicate: Communicate with other agents in the environment
    - get_observation: Get the observation of the agent - update the observation space
    - get_action: Get the action of the agent - the next position to move to

    ### Properties
    - agent_id: ID of the agent
    - position: Position of the agent in the environment
    - communication_range: Communication range of the agent
    - visited_junctions: List of junctions visited by the agent
    - belief_state: Belief state of the agent
    """
    # Constructor for the greedy agent class
    def __init__(self, environment, agent_id, position, communication_range=1):
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
        self.visited_junctions = []

        # Check if the position is in the network environment and a junction
        if self.position not in environment.junction_names:
            raise ValueError(f'Position {self.position} is not in the network environment')

        # Check if the position is in the adjacency list
        if self.position not in environment.get_adj_list().keys():
            raise KeyError(f'Position {self.position} is not in adjacency list')

        # Construct agents belief state containing the position and a dictionary of nodes 
        # and their states (default to None)
        self.belief_state = {
            'position': self.position,
            'node_belief': {node: None for node in environment.get_adj_list().keys()},
            'planned_path': []
        }

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
        # Other agents simply send across their belief states or observations?
        # Probably just their belief states as they are derived from their observations 
        # and any information communicated to them - information can propagate through the network
        pass

    def get_observation(self, environment, other_agents=None):
        """
        Method to get the observation of the agent - update the observation space
        ---
        :param environment: Environment in which the agent is observing - the pipe network
        :param other_agents: Other agents in the environment

        :return: Observation of the agent
        """

        # Get the observation space
        observation = {
            'position': self.position,
            'visited_junctions': self.visited_junctions,
            'pipe_network_state': environment.get_state(self.position),
            'other_agents': other_agents
        }

        # Log the agent's observation (position and pipe network state)
        self.log.info(f"Agent {self.agent_id} is at {observation['position']}")
        self.log.info(f"Agent {self.agent_id} is observing {observation['pipe_network_state']}")

        # Update the agent's belief state
        self.update_belief_state(observation)

        return observation

    def update_belief_state(self, observation):
        """
        Method to update the agent's belief state
        ---
        Explored junctions have belief value = 0
        Unexplored junctions have belief value = 1
        Occupied junctions (with other agents) have belief value = -10
        :param observation: Observation of the agent
        :return: None
        """
        # create temporary deepcopy of the beleif state before it has been updated with the new observation
        temp_belief_state = copy.deepcopy(self.belief_state)

        # update the position of the agent in the belief state
        temp_belief_state['position'] = observation['position']

        # update the node_belief for the current position as explored
        temp_belief_state['node_belief'][observation['position']] = 0

        # compare observsation['pipe_network_state'] with current belief state 
        # to see if any junctions are unexplored
        for junction in observation['pipe_network_state']:
            # if the agent has no information about the junction (None) then set it to unexplored (1)
            if temp_belief_state['node_belief'][junction] is None:
                temp_belief_state['node_belief'][junction] = 1
            # if the agent has information about the junction (0) then set it to explored (0)
            elif temp_belief_state['node_belief'][junction] == 0:
                temp_belief_state['node_belief'][junction] = 0
            # TODO: Case in which the agent has information about the junction (-10) - requires comms
                

        # keep track of the junctions that have been visited in the belief state
        temp_belief_state['node_belief'][observation['position']] = 0

        # compare observation['other_agents'] with current belief state
        # to see if any junctions are occupied
        for agent in observation['other_agents']:
            if temp_belief_state['node_belief'][agent.position] is None:
                temp_belief_state['node_belief'][agent.position] = -10

    def get_action(self, observation):
        """
        Method to get the action of the agent - update the action space
        :param observation: Observation of the agent
        :return: Action of the agent
        """

        # Get the action space
        adjacent_nodes = observation['pipe_network_state']

        # Get the unvisited adjacent nodes
        unvisited_adjacent_nodes = [node for node in adjacent_nodes if node not in observation['visited_junctions']]

        # Get the action space
        action_space = {
            'adjacent_nodes': adjacent_nodes,
            'unvisited_adjacent_nodes': unvisited_adjacent_nodes
        }

        action = self.greedy_action(action_space)

        # Log the agent's action
        self.log.info(f"Agent {self.agent_id} is taking action {action}")

        return action

    def get_visited_junctions(self):
        """
        Method to get the visited nodes
        :return: Visited nodes
        """
        return self.visited_junctions

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