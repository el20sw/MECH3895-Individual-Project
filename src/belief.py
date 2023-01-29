# Import modules
import debug.logger as logger

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

    def update(self, environment, action, observation) -> None:
        """
        Update the belief state of the agent
        :param environment: Environment in which the agent is operating - the pipe network
        :param action: Action taken by the agent
        :param position: Position of the agent in the environment
        """

        # Update the agent _position
        self._position = action

        # Update the node status of the new node to visited
        self._nodes[self._position] = 0

        # Update the nodes in the observation
        # TODO: Update the node status based on the observation

        # Update the links
        self._links.extend(environment.get_links(self._position))
        # Remove duplicate links
        self._links = list(set(self._links))

        """
        if there is transmittables in the observation, create local copies of all the transmittables
        compare with the agents current belief state
        update the belief state with the new information
        """

    # Class method to create a belief state from a dictionary
    @classmethod
    def from_dict(cls, belief_dict):
        """
        Create a belief state from a dictionary
        :param belief_dict: Dictionary containing the belief state
        :return: Belief state object
        """
        belief = cls(belief_dict['_environment'])
        belief._agent_id = belief_dict['_agent_id']
        belief._position = belief_dict['_position']
        belief._nodes = belief_dict['_nodes']
        belief._links = belief_dict['_links']
        return belief