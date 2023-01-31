# Import modules
import src.debug.logger as logger

from typing import Optional, Union

from src.observation import Observation
from src.transmittable import Transmittable

### Agent Belief States ###
class Belief:
    """
    Agent Belief State Class
    ----------
    Class for agent belief states - each agent has a belief state using which it makes
    decisions

    :param environment: Environment in which the agent is operating - the pipe network
    :param agent_id: ID of the agent
    :param position: Position of the agent in the environment (likely to be the starting position)
    
    note: this is used to initialise the belief state nodes creating a dictionary with
    node names as keys and node status as values

    The belief state contains the following information:
    - Agent ID: ID of the agent
    - Position: Position of the agent in the environment
    - Nodes: List of nodes in the environment and their status
        - Status: 0 - Visited, 1 - Unvisited, -10 - Occupied
    - Links: List of links in the environment known to the agent
        - Links are given as a tuple of the form (node1, node2, length)
        - Agent can use the links to identify a path between two nodes anywhere in
        the known environment
    """

    def __init__(self, environment, agent_id=None, position=None) -> None:
        """
        Constructor for the agent belief state class
        :param environment: Environment in which the agent is operating - the pipe network
        :param agent_id: ID of the agent
        :param position: Position of the agent in the environment (likely to be the starting position)

        On initialisation, the agent's belief state contains the following information:
        - Agent ID: ID of the agent
        - Position: Position of the agent in the environment
        - Nodes: List of nodes in the environment and their status - all nodes are unvisited by default except the starting node which is visited
        - Links: List of links in the environment known to the agent - empty by default

        :return: None

        """
        # Initialise the logger
        self.log = logger.setup_logger(__name__, 'logs/belief.log')

        # Initialise the belief state
        self._agent_id = agent_id
        self._position = position
        self._nodes = {node: 1 for node in environment.adj_list.keys()}    # all nodes are unvisited by default
        # update node status of the starting node to visited
        self._nodes[self._position] = 0
        self._links = []

        self._environment = environment
    
    @property
    def agent_id(self):
        """
        Agent ID getter
        :return: Agent ID
        """
        return self._agent_id

    @property
    def position(self):
        """
        Position getter
        :return: Position
        """
        return self._position

    @property
    def nodes(self):
        """
        Nodes getter
        :return: Nodes
        """
        return self._nodes

    @property
    def links(self):
        """
        Links getter
        :return: Links
        """
        return self._links

    def update(self, *information : Union[Observation, Transmittable]):
        """
        Update the belief state of the agent
        :param information: Information received by the agent - may be multiple communications and/or the observation
        :param observation: Observation of the agent
        :param communication: Communication received from other agents - may be multiple transmittable objects
        :return: None
        """

        # Order of precedence for updating the node status:
        # 1. Occupied (-10)
        # 2. Visited (0)
        # 3. Unvisited (1)

        # Extract the observation and communication from the information
        observation = None
        communication = []

        for info in information:
            # If the information is an observation, extract the observation
            if isinstance(info, Observation):
                observation = info
            # If the information is a transmittable object, extract the communication and add to comms list
            elif isinstance(info, Transmittable):
                communication.append(info)
            # If the information is neither an observation nor a transmittable object, raise an error
            else:
                e = ValueError(f"Information {info} is type {type(info)} and not an observation or a transmittable object")
                self.log.error(e)
                raise e

        # Update the belief state from the observation
        if observation is not None:
            self._update_from_observation(observation)

        # Update the belief state from the communication
        if communication:
            self._update_from_communication(*communication)        

    # Method to update from the observation
    def _update_from_observation(self, observation : Observation):
        """
        Method to update the belief state from the observation
        :param observation: Observation of the agent
        :return: None
        """
        
        # Make a reference to the previous position
        prev_position = self._position
        # Update the agent's position
        self._position = observation.position

        # If the previous position is not the same as the current position, create a link tuple
        if prev_position != self._position:
            link = self._create_link(self._position, prev_position)
            # Add the link to the list of links if it is not already present
            if link not in self._links:
                self._links.append(link)

        # Extract the node and neighbour information from the observation
        node = observation.state['node']
        neighbours = observation.state['neighbours']

        # Node should be the same as the agent's position
        if node != self._position:
            raise ValueError(f"Node {node} is not the same as the agent's position {self._position}")

        # Update the node status to visited
        self._nodes[node] = 0

        # Update the belief state with the local observation
        for neighbour in neighbours:
            # If the neightbour has not been visited or there is no information about the neighbour, set the status to unvisited
            if self._nodes[neighbour] == 1 or self._nodes[neighbour] is None:
                self._nodes[neighbour] = 1

    # Method to update from the communication
    def _update_from_communication(self, *communication : Transmittable):
        """
        Method to update the belief state from communication
        :param communication: Communication received from other agents - may be multiple transmittable objects
        :return: None
        """
        # For each communication object, unpack the contained objects
        for transmittable in communication:
            objects = transmittable.objects
            # Find the object of type Belief
            for obj in objects:
                if isinstance(obj, Belief):
                    # Update the belief state with the received belief state
                    self._update_belief_state(obj)
                else:
                    # Log the error
                    self.log.error(f"Object {obj} is not of type Belief")

    # Method to create link tuple from node and previous node
    def _create_link(self, node, prev_node):
        """
        Create a link tuple from node and previous node
        :param node: Node
        :param prev_node: Previous node
        :return: Link tuple
        """
        return (node, prev_node, self._environment.adj_list[node][prev_node])


    # Method to update the belief state with the received belief state
    def _update_belief_state(self, belief_state):
        """
        Update the belief state with the received belief state
        :param belief_state: Received belief state
        :return: None
        """

        # Get the position of the agent from the received belief state
        position = belief_state.position
        # Set the node status of the position to occupied
        self._nodes[position] = -10

        # Get the nodes and links from the received belief state
        nodes = belief_state.nodes
        links = belief_state.links

        # Update the nodes in the belief state - visited nodes override unvisited nodes and occupied nodes override both unless occupied node is the current position
        for node, status in nodes.items():
            if node == self._position:
                self._nodes[node] = 0
            elif status == -10:
                self._nodes[node] = -10
            elif status == 0:
                self._nodes[node] = 0
            elif status == 1:
                if self._nodes[node] == 1 or self._nodes[node] is None:
                    self._nodes[node] = 1

        # Update the links in the belief state - a tuple of form (node1, node2, length)
        for link in links:
            if link not in self._links:
                self._links.append(link)
