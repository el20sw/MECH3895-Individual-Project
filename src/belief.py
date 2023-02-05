# Import modules
import src.debug.logger as logger

from copy import deepcopy
from typing import Optional, Union, List

from src.observation import Observation
from src.transmittable import Transmittable

OCCUPIED = -10
VISITED = 0
UNVISITED = 1

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
        - Other agents: Dictionary of other agents in the enviroment and last known positions - empty by default

        :return: None

        """
        # Initialise the logger
        self._log = logger.get_logger(__name__)

        # Initialise the belief state
        self._agent_id = agent_id
        self._position = position
        self._nodes = {node: UNVISITED for node in environment.adj_list.keys()}    # all nodes are unvisited by default
        self._other_agents = {}
        
        # update node status of the starting node to VISITED
        self._nodes[self._position] = VISITED
        self._links = []

        self._environment = environment
        self._occupied_nodes = [node for node in self._nodes.keys() if self._nodes[node] == OCCUPIED]
        self._visited_nodes = [node for node in self._nodes.keys() if self._nodes[node] == VISITED]
        self._unvisited_nodes = [node for node in self._nodes.keys() if self._nodes[node] == UNVISITED]

        self._other_agent_positions = []
        self._persistent_unvisited_neighbours = {}
        self._other_agents_unvisited_neighbours = {}

    def __repr__(self) -> str:
        """
        Representation of the agent belief state
        :return: Representation of the agent belief state
        """
        return f'Agent {self._agent_id} Belief'
        
    def __str__(self) -> str:
        """
        String representation of the agent belief state
        :return: String representation of the agent belief state
        """
        return f'Agent {self._agent_id} Belief'

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
    def unvisited_nodes(self):
        """
        Unvisited nodes getter
        :return: Unvisited nodes
        """
        return self._unvisited_nodes

    @property
    def visited_nodes(self):
        """
        Visited nodes getter
        :return: Visited nodes
        """
        return self._visited_nodes

    @property
    def occupied_nodes(self):
        """
        Occupied nodes getter
        :return: Occupied nodes
        """
        return self._occupied_nodes

    @property
    def links(self):
        """
        Links getter
        :return: Links
        """
        return self._links

    @property
    def other_agents(self):
        """
        Other agents getter
        :return: Other agents
        """
        return self._other_agents

    @property
    def persistent_unvisited_neighbours(self):
        """
        Persistent unvisited neighbours getter
        :return: Persistent unvisited neighbours
        """
        return self._persistent_unvisited_neighbours

    @property
    def other_agents_unvisited_neighbours(self):
        """
        Other persistent unvisited neighbours getter
        :return: Other persistent unvisited neighbours
        """
        return self._other_agents_unvisited_neighbours

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
        communication: List[Transmittable] = []

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
                self._log.error(e)
                raise e

        # Update the belief state from the observation
        if observation is not None:
            self._update_from_observation(observation)

        # Update the belief state from the communication
        if communication:
            self._update_from_communication(*communication)

        # Log the belief state
        self._log.debug(f"Agent {self._agent_id} belief state: {self._nodes}")

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
                self._log.debug(f"Agent {self._agent_id} added link {link} to the list of links")

        # Extract the node and neighbour information from the observation
        node = observation.state['node']
        neighbours = observation.state['neighbours']

        # Node should be the same as the agent's position
        if node != self._position:
            raise ValueError(f"Node {node} is not the same as the agent's position {self._position}")

        # Update the node status to VISITED
        self._nodes[node] = VISITED
        self._log.debug(f"Agent {self._agent_id} updated node {node} to visited")

        # Update the list of visited nodes
        self._visited_nodes = [node for node in self._nodes.keys() if self._nodes[node] == VISITED]
        # Update the list of unvisited nodes
        self._unvisited_nodes = [node for node in self._nodes.keys() if self._nodes[node] == UNVISITED]
        # Update the list of occupied nodes
        self._occupied_nodes = [node for node in self._nodes.keys() if self._nodes[node] == OCCUPIED]

        # Update the belief state with the local observation
        for neighbour in neighbours:
            # If the neightbour has not been visited or there is no information about the neighbour, set the status to unvisited
            if self._nodes[neighbour] == UNVISITED or self._nodes[neighbour] is None:
                self._nodes[neighbour] = UNVISITED
                self._log.debug(f"Agent {self._agent_id} updated node {neighbour} to unvisited")

    # Method to update from the communication
    def _update_from_communication(self, *communication : Transmittable):
        """
        Method to update the belief state from communication
        :param communication: Communication received from other agents - may be multiple transmittable objects
        :return: None
        """

        belief_stack = []

        # For each communication object, unpack the contained objects
        for transmittable in communication:
            objects = transmittable.objects
            # Find the object of type Belief
            for obj in objects:
                if isinstance(obj, Belief):
                    # Add to the belief stack
                    # self._update_belief_state(obj)
                    belief_stack.append(obj)
                else:
                    # Log the error
                    self._log.error(f"Object {obj} is not of type Belief")
                    continue

        # make a copy of the other agents dictionary
        other_agents_new = deepcopy(self._other_agents)
        # make a copy of the nodes dictionary
        nodes_new = deepcopy(self._nodes)

        # Update the belief state from the other agents visited nodes
        nodes_new = self._visited_handler(belief_stack, nodes_new)
        # Update the belief state from the other agents positions
        nodes_new, other_agents_new = self._position_handler(belief_stack, nodes_new, other_agents_new)

        self._nodes = nodes_new
        self._other_agents = other_agents_new

        # destroy the copies
        del other_agents_new
        del nodes_new

        # Update the list of visited nodes
        self._visited_nodes = [node for node in self._nodes.keys() if self._nodes[node] == VISITED]
        # Update the list of unvisited nodes
        self._unvisited_nodes = [node for node in self._nodes.keys() if self._nodes[node] == UNVISITED]
        # Update the list of occupied nodes
        self._occupied_nodes = [node for node in self._nodes.keys() if self._nodes[node] == OCCUPIED]

        # Update the links
        for belief in belief_stack:
            # Get the nodes and the links from this agents belief state
            this_belief_links = self._links
            # Get the nodes and links from the received belief state
            other_belief_links = belief.links
            # Update the links
            self._update_links(this_belief_links, other_belief_links)
            # add to dictionary of other agents persistent unvisited neighbours
            self._update_other_agents_unvisited_neighbours(belief)

    def _position_handler(self, belief_stack, nodes_new, other_agents_new):
        """
        Method to handle the beliefs of agent positions 
        :param belief_stack: Stack of beliefs received from other agents
        :param nodes_new: Copy of the nodes dictionary
        :param other_agents_new: Copy of the other agents dictionary
        :return: Updated nodes dictionary and updated other agents dictionary
        """

        # extract the agent positions from the beliefs in the belief stack and update the other agents dictionary for agents in range
        self._log.debug(f'{self._agent_id}: Previous agent positions: {self._other_agents}')
        other_agents_new = self._update_other_agents(belief_stack)
        self._log.debug(f'{self._agent_id}: Updated agent positions: {other_agents_new}')

        # compare the previous agent positions to the new agent positions
        for id, position in other_agents_new.items():
            # if the agent is out of range, set the old position to visited
            if position is None:
                old_position = self._other_agents[id]
                if old_position is not None:
                    nodes_new[old_position] = VISITED
                    self._log.debug(f'{self._agent_id}: Updated node {old_position} to visited')
            # if the agent is in range, set the new position to occupied and the old position to visited
            else:
                nodes_new[position] = OCCUPIED
                self._log.debug(f'{self._agent_id}: Updated node {position} to occupied')
                old_position = self._other_agents.get(id, None)
                if old_position is not None:
                    nodes_new[old_position] = VISITED
                    self._log.debug(f'{self._agent_id}: Updated node {old_position} to visited')
                else:
                    self._log.info(f'{self._agent_id}: No old position for agent {id}')    
    
        return (nodes_new, other_agents_new)

    def _update_other_agents(self, belief_stack):
        """
        Method to update the other agents in the belief state based on received positions
        :param belief_stack: Stack of beliefs
        :return: None
        """

        # create a copy of the other agents dictionary
        other_agents_new = deepcopy(self._other_agents)

        for belief in belief_stack:
            # If first contact!
            if belief.agent_id not in other_agents_new.keys():
                other_agents_new[belief.agent_id] = belief.position
                self._log.debug(f"Agent {self._agent_id} added agent {belief.agent_id} to the list of other agents")
            # Or if renewed contact
            elif other_agents_new[belief.agent_id] is None:
                other_agents_new[belief.agent_id] = belief.position
                self._log.debug(f"Agent {self._agent_id} updated agent {belief.agent_id} to position {belief.position}")
            # Otherwise
            else:
                for id, position in other_agents_new.items():
                    # If the agent is in range, update the position
                    if id == belief.agent_id:
                        other_agents_new[id] = belief.position
                        self._log.debug(f"Agent {self._agent_id} updated agent {id} to position {belief.position}")
                    # Otherwise, set the position to None
                    else:
                        other_agents_new[id] = None
                        self._log.debug(f"Agent {self._agent_id} updated agent {id} to position {None}")

        # return the copy
        return other_agents_new

    def _visited_handler(self, belief_stack, nodes_new):
        """
        Method to handle the beliefs of visited nodes
        :param belief_stack: Stack of beliefs
        :param nodes_new: Copy of the nodes dictionary
        :return: Updated nodes dictionary
        """
        self._log.debug(f'{self._agent_id}: Previous visited nodes: {self._visited_nodes}')

        visited_nodes = []
        
        for belief in belief_stack:
            for node, status in belief.nodes.items():
                if status == VISITED:
                    visited_nodes.append(node)
                    nodes_new[node] = VISITED
                    self._log.debug(f'{self._agent_id}: Updated node {node} to visited')

        
        self._log.debug(f'{self._agent_id}: Updated visited nodes: {visited_nodes}')

        return nodes_new

    def _update_links(self, this_belief_links, other_belief_links):
        """
        Update the links in the belief state
        :param this_belief_links: Links in this belief state
        :param other_belief_links: Links in the received belief state
        :return: None
        """
        for link in other_belief_links:
            if link not in this_belief_links:
                self._links.append(link)
                self._log.debug(f"Agent {self._agent_id} added link {link} to the list of links")

    # Method to create link tuple from node and previous node
    def _create_link(self, node, prev_node):
        """
        Create a link tuple from node and previous node
        :param node: Node
        :param prev_node: Previous node
        :return: Link tuple
        """
        return (node, prev_node, self._environment.adj_list[node][prev_node])


    def _update_persistent_unvisited_neighbours(self, neighbour, position):
        """
        Method to update the persistent unvisited neighbours dictionary
        :param neighbour: Unvisited neighbour
        :return: None
        """

        # check if position is equal to the current position
        if position != self._position:
            self._log.critical(f"Agent {self._agent_id} has different belief position {self._position} to actual position {position}")

        if neighbour in self._persistent_unvisited_neighbours.keys():
            self._persistent_unvisited_neighbours[neighbour].append(position)
        else:
            self._persistent_unvisited_neighbours[neighbour] = [position]
            
        self._log.debug(f"Agent {self._agent_id} has found an unvisited node {neighbour} in the action space")
        self._log.debug(f"Agent {self._agent_id} has persistent unvisited neighbours: {self._persistent_unvisited_neighbours}")

    def _update_other_agents_unvisited_neighbours(self, other_agents_belief):
        """
        Method to update the other agents unvisited neighbours dictionary
        :param other_agents_belief: Other agents belief state
        :return: None
        """

        other_agent_id = other_agents_belief.agent_id
        other_agents_persistent_unvisited_neighbours = other_agents_belief.persistent_unvisited_neighbours

        if other_agent_id in self._other_agents_unvisited_neighbours.keys():
            self._other_agents_unvisited_neighbours[other_agent_id].update(other_agents_persistent_unvisited_neighbours)
        else:
            self._other_agents_unvisited_neighbours[other_agent_id] = other_agents_persistent_unvisited_neighbours

        # log the other agents unvisited neighbours
        self._log.debug(f"Agent {self._agent_id} has other agents unvisited neighbours: {self._other_agents_unvisited_neighbours}")
